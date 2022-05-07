"""
Given a specific file path on Secretary of State website, downloads file, parses data, and saves ZIP-code level EV data
"""
import os

import pandas as pd
import pycurl
from io import BytesIO
import pdfplumber
import re

SOS_EV_FILE = 'https://www.ilsos.gov/departments/vehicles/statistics/electric/home.html'

# TODO: download and save to data directory
buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, SOS_DIR)

# TODO: add linting

# TODO: read from correct data path
pdf_data = '/Users/robert/Learnings/il-ev-counts/data/electric041522.pdf'

# extract EV counts by ZIP code
pdf = pdfplumber.open(pdf_data)
ev_df = pd.DataFrame(columns=['municipality', 'zip_code', 'ev_count'])
# TODO first two pages need special treatment
# parse pages with uniform layout
for page in pdf.pages[2:]:
    text = page.extract_text()
    lines = text.split('\n')
    line_split = [re.split(r'\s{3,}', line) for line in lines]
    temp_df = pd.DataFrame(line_split, columns=['district', 'zip_code', 'ev_count'])
    ev_df = pd.concat([ev_df, temp_df])

# TODO: remove whitespace
# TODO: remove last row


# TODO: save final file as a csv
