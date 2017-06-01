from bs4 import BeautifulSoup

import requests


def get_web_page(url):
    resp = requests.get(
        url=url,
        #cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom):
    soup = BeautifulSoup(dom, 'html.parser')

    articles = []  # 儲存取得的文章資料
    trs = soup.find_all('tr', 'rowlink')
    for t in trs:
        # 取得打擊率、上壘率、長打率
        tds = t.find_all('td')

        avg = tds[13].string
        obp = tds[14].string
        slg = tds[15].string
        name = tds[2].find('a').string

        articles.append(avg)
        articles.append(obp)
        articles.append(slg)
        articles.append(name)

    return articles

