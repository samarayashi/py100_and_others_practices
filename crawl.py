import requests
import os
from constants import fnames, file_dir

domain_url = 'https://plvr.land.moi.gov.tw/'
season = '108S2'


if not os.path.exists(file_dir):
    os.makedirs(file_dir)

for fname in fnames:
    response = requests.get(
        f'{domain_url}/DownloadSeason?season={season}&fileName={fname}')

    fpath = os.path.join(file_dir, fname)
    with open(fpath, 'wb') as file:
        file.write(response.content)
