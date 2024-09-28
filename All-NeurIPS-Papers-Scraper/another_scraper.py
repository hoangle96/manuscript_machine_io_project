import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from tqdm import tqdm
import pandas as pd

def parse_paper_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # The following is not a nice or robust way to filter papers and is prone to 
    # break if the website layout should change, but is sufficient for a demo
    info = {}
    info["title"] = soup.findAll("h4")[0].text
    info["authors"] = soup.findAll("i")[-1].text
    info["abstract"] = soup.findAll("p")[2].text
    info["url"] = url
    return info

if __name__ == '__main__':
    response = requests.get("https://papers.nips.cc/paper/2021")
    # Parse the response as HTML
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all the <a> tags on the page (these contain the links)
    links = soup.find_all("a")
    abstract_links = []
    # Print the URLs of the links
    for link in links:
        if "-Abstract.html" in link["href"]:  # Filter the abstracts
            abstract_links.append("https://papers.nips.cc" + link["href"])
    print(f"{len(abstract_links)} abstracts found")

    results = []
    with Pool(4) as pool:  # Execute commands in parallel to speed things up
        for result in tqdm(pool.imap_unordered(parse_paper_page, abstract_links)):
            results.append(result)


    df = pd.DataFrame(results)
    df.to_csv('neurips_2021.csv')

