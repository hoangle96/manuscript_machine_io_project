import os
import sys
import json
import argparse
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type



# Data fetch function
default_headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}


base_url = "https://papers.nips.cc"



############################################## Fetching Functions ##############################################################

@retry(retry=retry_if_exception_type(aiohttp.ClientError), stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch(session, url):
    try:
        async with session.get(url, headers=default_headers) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None

async def fetch_all(session, urls):
    tasks = [fetch(session, url) for url in urls]
    return await asyncio.gather(*tasks)


############################################## Helper Functions ##############################################################
def get_conference_url(year):
    return f"{base_url}/paper/{year}"

async def fetch_latest_conference_year():
    url = 'https://papers.nips.cc/'
    async with aiohttp.ClientSession() as session:
        page_content = await fetch(session, url)
        if page_content is None:
            return 2023
        soup = BeautifulSoup(page_content, 'html.parser')

        years = []
        for item in soup.find_all('li'):
            try:
                year = int(item.text.split()[-1].strip('()'))
                years.append(year)
            except (ValueError, IndexError):
                continue

    return max(years) if years else 2023



async def get_paper_paths(session, year):
    url = get_conference_url(year)
    page_content = await fetch(session, url)
    if page_content is None:
        return [], [], [], []
    soup = BeautifulSoup(page_content, "html.parser")
    
    paper_ids, abstract_paths, metadata_paths, pdf_paths = [], [], [], []

    for li in soup.find("div", class_='container-fluid').find_all("li"):
        paper_temp_url = li.a.get('href')
        paper_id = paper_temp_url.split("/")[-1].split("-")[0]
        
        paper_ids.append(paper_id)
        abstract_paths.append(f"{base_url}{paper_temp_url}")
        
        paper_base_url = f"{base_url}{paper_temp_url.rsplit('.', 1)[0]}"
        metadata_paths.append(f"{paper_base_url.replace('Abstract', 'Metadata').replace('hash', 'file')}.json")
        pdf_paths.append(f"{paper_base_url.replace('Abstract', 'Paper').replace('hash', 'file')}.pdf")
    
    return paper_ids, abstract_paths, metadata_paths, pdf_paths


######################################## Arguments and checks ################################################################
def get_args(latest_year):
    parser = argparse.ArgumentParser(description='Download NIPS papers')
    parser.add_argument('--start_year', type=int, default=2017, help='start year')
    parser.add_argument('--end_year', type=int, default=latest_year, help='end year')
    parser.add_argument('--output_dir', type=str, default='data', help='output directory')
    parser.add_argument('--type', type=str, choices=['metadata', 'pdf', 'abstract', 'all'], default='all', help='Type of data to download (metadata, pdf, abstract, all)')
    parser.add_argument('--verbose', action='store_true', help='verbose mode', default=False)
    return parser.parse_args()

def check_args(args):
    if args.start_year < 1987:
        sys.exit("Start year must be 1987 or later")
    if args.start_year > args.end_year:
        sys.exit("Start year must be less than or equal to end year")



############################################# Fetch, Save and Download Functions #############################################
@retry(retry=retry_if_exception_type(aiohttp.ClientError), stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_metadata(session, meta_path):
    async with session.get(meta_path) as response:
    
        if response.status != 200: # 200 is the status code for successful HTTP requests
            return {}
        return await response.json()

@retry(retry=retry_if_exception_type(aiohttp.ClientError), stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_pdf(session, pdf_path):
    try:
        async with session.get(pdf_path) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        print(f"Error downloading PDF from {pdf_path}: {e}")
        return None
@retry(retry=retry_if_exception_type(aiohttp.ClientError), stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_abstract(session, abstract_path):
    async with session.get(abstract_path) as response:
        if response.status != 200: 
            return ""
        soup = BeautifulSoup(await response.text(), "html.parser")
        abstract_text = soup.find('h4', string='Abstract').find_next('p').get_text()
        abstract_text = " ".join(abstract_text.split())
        title = soup.find('meta', {'name': 'citation_title'})['content']
        authors = soup.find_all('meta', {'name': 'citation_author'})
        authors = [author['content'] for author in authors]
        return {'title': title, 'authors': authors, 'abstract': abstract_text}


############################################### Main functions ###############################################################


async def download_papers_for_year(session, year, output_dir, download_type, verbose=False):
    paper_ids, abstract_paths, metadata_paths, pdf_paths = await get_paper_paths(session, year)
    # print(len(paper_ids), len(abstract_paths), len(metadata_paths), len(pdf_paths))

    for paper_id, abstract_path, metadata_path, pdf_path in tqdm(zip(paper_ids, abstract_paths, metadata_paths, pdf_paths), desc=f"Year {year}"):

        if verbose:
            print(f"Downloading {paper_id} from {year}")

        save_dir = os.path.join(output_dir, str(year), paper_id)
        os.makedirs(save_dir, exist_ok=True)

        if download_type in ['metadata', 'all']:
            metadata = await get_metadata(session, metadata_path)
            with open(os.path.join(save_dir, f"{paper_id}_metadata.json"), "w") as f:
                json.dump(metadata, f, indent=4)
        
        if download_type in ['pdf', 'all']:
            pdf = await get_pdf(session, pdf_path)
            if pdf:
                with open(os.path.join(save_dir, f"{paper_id}.pdf"), "wb") as f:
                    f.write(pdf)
        
        if download_type in ['abstract', 'all']:
            abstract = await get_abstract(session, abstract_path)
            with open(os.path.join(save_dir, f"{paper_id}_abstract.json"), "w") as f:
                json.dump(abstract, f, indent=4)

        await asyncio.sleep(0.2) # to avoid getting blocked by the server













