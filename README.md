### Illinois EV Registrations Parser

The goal of this package is to download EV registration data PDFs from Illinois Secretary of 
State website, parse the PDF into a dataframe, and save the EV registration counts by zip code as a CSV file.

SOS Website: https://www.ilsos.gov/departments/vehicles/statistics/electric/home.html 

Prerequisites
- python 3.9 and poetry installed on local machine
- to install poetry using homebrew, run `brew install poetry`
- to enable poetry environment by running `poetry env use python 3.9`

To run code:
- `python3 run query_registration_data.py <URL>`
- example URL: https://www.ilsos.gov/departments/vehicles/statistics/electric/2022/electric011522.pdf