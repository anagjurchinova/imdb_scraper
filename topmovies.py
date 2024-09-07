import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

baseurl = 'https://www.imdb.com'
targeturl = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'

time.sleep(2)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}
page = requests.get(targeturl, headers=headers)
soup = BeautifulSoup(page.content, 'lxml')
show_links = soup.findAll('a', class_='ipc-title-link-wrapper')

shows_list = []

for link in show_links:
    show_url = baseurl + link['href']
    page = requests.get(show_url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    title = soup.find('span', class_='hero__primary-text').text.strip()
    description = soup.find('div', class_='ipc-html-content-inner-div').text.strip()
    genre = soup.find('a', class_='ipc-metadata-list-item__list-content-item').text.strip()

    show = {
        'title': title,
        'description': description,
        'genre': genre
    }
    shows_list.append(show)

df = pd.DataFrame(shows_list)
print(df.head(5))
