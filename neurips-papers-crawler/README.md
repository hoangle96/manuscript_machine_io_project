## NeurIPS Papers Crawler 

This project is designed to curate the research papers for the language models, specific to the NeurIPS conference website from 1987 to the latest conference. The web scrapper fetches paper metadata (for years before 2020), summaries, and PDFs for either a given year or a specific range of years. 


```bash
project_root/
├── data
│   ├── 2021
│   │   ├── paper_id
│   │   │   ├── paper_id_abstract.json
│   │   │   ├── paper_id_metadata.json
│   │   │   └── paper_id.pdf
│   └── ...
├── utils.py
├── crawler.py
├── requirements.txt
├── Readme.md
```
## Installation
To install this crawler, Ensure you have Python 3.7 or later installed. 
You will also need to install the required Python packages:

``` bash
pip install -r requirements.txt
```

## Usage
To execute the crawler use the following command.

```bash
python crawler.py --start_year 2020 --end_year 2021 --output_dir './data/' --type 'all'
```
Arguments for the crawler:
* --start_year: The starting year of the conference papers you want to download (default is 1987).
* --end_year: The ending year of the conference papers you want to download (default is the latest year available).
* --output_dir: The directory where the data will be saved (default is data).
* --type: To download the specific data type., it takes 'metadata', 'pdf', 'abstract', 'all' as inputs (default is all)


## Notes
1) Ensure the output directory exists before running the script.
2) The script fetches data concurrently to speed up the process.
3) If any errors occur while fetching the data, error message will be shown and exit out. 
