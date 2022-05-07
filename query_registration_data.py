""" Given a specific file path on Secretary of State website, downloads file,
parses data, and saves ZIP-code level EV data
"""
import os

import pandas as pd
from io import BytesIO
import pdfplumber
import re

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
ev_df = ev_df[~ev_df['ev_count'].isna()]
ev_df['ev_count'] = ev_df['ev_count'].astype(int)

# TODO: check that total count matches total count in PDF
ev_df.to_csv(cwd + '/data/ev_counts_by_zipcode.csv', index=False)
