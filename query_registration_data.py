""" Given a specific file path on Secretary of State website, downloads file,
parses data, and saves ZIP-code level EV data
"""
import os

import pandas as pd
from io import BytesIO
import pdfplumber
import re
import logging

LOGGER = logging.getLogger()
SOS_EV_FILE = 'https://www.ilsos.gov/departments/vehicles/statistics/electric/home.html'

# TODO: download and save to data directory
# buffer = BytesIO()
# c = pycurl.Curl()
# c.setopt(c.URL, SOS_DIR)

# TODO: add linting

cwd = os.getcwd()
pdf_data = 'electric041522.pdf'

# extract EV counts by ZIP code
pdf = pdfplumber.open(cwd + f'/data/{pdf_data}')
ev_df = pd.DataFrame(columns=['municipality', 'zip_code', 'ev_count'])

# parse pages with uniform layout - skipping first page
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
    LOGGER.warning(f"Derived EV count of {ev_df['ev_count'].sum()} does not match provided total of {total_ev_count}")

ev_df.to_csv(cwd + '/data/ev_counts_by_zipcode.csv', index=False)
