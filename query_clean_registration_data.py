""" Given a specific file path on Secretary of State website, downloads file,
parses data, and saves ZIP-code level EV data

Sample URL: 'https://www.ilsos.gov/departments/vehicles/statistics/electric/2022/electric041522.pdf'
"""
import os
import sys
import pandas as pd
import requests
import pdfplumber
import re
import logging


def download_ev_data(url: str, filename: str):
    # download and save PDF from Secretary of state website
    response = requests.get(url)
    open(f"{cwd}/data/{filename}.pdf", "wb").write(response.content)


def convert_ev_data(filename: str):
    # extract EV counts by ZIP code
    pdf = pdfplumber.open(cwd + f'/data/{filename}.pdf')

    # parse pages with uniform layout - skipping first page
    ev_df = pd.DataFrame(columns=['municipality', 'zip_code', 'ev_count'])
    for page in pdf.pages[1:]:
        text = page.extract_text()
        lines = text.split('\n')
        line_split = [re.split(r'\b\s{2,}', line) for line in lines]
        temp_df = pd.DataFrame(line_split, columns=['municipality', 'zip_code', 'ev_count'])
        cutoff_idx = temp_df.index[temp_df['municipality'].str.contains('ZIPCODE TOTALS', na=False)].tolist()
        if cutoff_idx:
            temp_df = temp_df.loc[cutoff_idx[0] + 1:]
        ev_df = pd.concat([ev_df, temp_df])

    # additional cleanup
    ev_df['municipality'] = ev_df['municipality'].str.strip()

    # extract total vehicle count from end of file for sanity checking
    total_ev_count = re.sub(r'(.+\s)', '', ev_df.tail(1)['zip_code'].values[0])

    ev_df = ev_df[~ev_df['ev_count'].isna()]
    ev_df['ev_count'] = ev_df['ev_count'].astype(int)

    if ev_df['ev_count'].sum() != int(total_ev_count):
        LOGGER.warning(f"Derived EV count of {ev_df['ev_count'].sum()} does not match "
                       f"provided total of {total_ev_count}")

    ev_df.to_csv(cwd + f'/data/ev_counts_{filename}.csv', index=False)


if __name__ == "__main__":
    logging.basicConfig()
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)

    ev_data_url = sys.argv[1]
    cwd = os.getcwd()
    file = ev_data_url.split('/')[-1].split('.')[0]
    download_ev_data(ev_data_url, filename=file)
    convert_ev_data(filename=file)
    LOGGER.info('Successfully converted EV registration PDF to CSV.')
