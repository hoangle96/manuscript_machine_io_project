"""
Bhuvan Chennoju
@linkedin: https://www.linkedin.com/in/bhuvanchennoju/
===================================================================================================
"""

import os
import sys
import asyncio
import aiohttp
from utils import fetch_latest_conference_year, get_args,check_args, download_papers_for_year

async def main():
    latest_year = await fetch_latest_conference_year()
    args = get_args(latest_year)
    check_args(args)
    start_year = args.start_year
    end_year = args.end_year
    output_dir = args.output_dir
    download_type = args.type
    verbose = args.verbose

    if not os.path.exists(output_dir):
        sys.exit(f"Output directory {output_dir} does not exist")

    async with aiohttp.ClientSession() as session:
        tasks = [download_papers_for_year(session, year, output_dir, download_type,verbose= verbose) for year in range(start_year, end_year + 1)]
        # if verbose:
        #     tasks = tqdm(tasks, desc="Years")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
