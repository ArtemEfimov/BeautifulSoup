import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    return r.status_code


def refined(s):
    return s.replace('$', '')


def write_csv(data):
    with open('cmc.csv12', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['number'],
                         data['name'],
                         data['symbol'],
                         data['price'],
                         data['url']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_='cmc-table__table-wrapper-outer').find('div').find_next('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        consecutive_number = tds[0].find('div', class_='').text
        name = tds[1].find('a', class_='cmc-link').text
        symbol = tds[5].find('div', class_='').text.split()[-2]
        price = tds[3].find('a', class_='cmc-link').text
        refined_price = refined(price)
        url = 'https://coinmarketcap.com' + tds[1].find('a').get('href')


        data = {'number': consecutive_number,
                'name': name,
                'symbol': symbol,
                'price': refined_price,
                'url': url}
        write_csv(data)


def main():
    url = 'https://coinmarketcap.com/'
    while True:
        html = get_html(url)
        get_page_data(html)
        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            pattern = 'Next'
            url = 'https://coinmarketcap.com/' + soup.find('div', class_='cmc-button-group va78v0-0 RDZiS').\
                find('a', text=re.compile(pattern)).get(
                'href')
        except:
            break


if __name__ == '__main__':
    main()
