import requests
# import csv
from bs4 import BeautifulSoup


# import re


def get_json(url):
    r = requests.get(url)
    return r.json()['data']


# def write_csv(data):
#     with open('shity_file.csv', 'a') as s:
#         order = ['number', 'name', 'symbol', 'price', 'url']
#         writer = csv.DictWriter(s, fieldnames=order)
#         writer.writerow(data)


def get_url(url2):
    r = requests.get(url2)
    return r.text


global_counter = 1


def get_data(d: dict):
    count = 0
    pattern = global_counter
    url2 = f'https://coinmarketcap.com/{pattern}/'
    html = get_url(url2)
    soup = BeautifulSoup(html, 'lxml')
    link = None
    for i in range(100):
        try:
            id = d[i]['id']
        except:
            id = ''
        try:
            name = d[i]['name']
        except:
            name = ''
        try:
            symbol = d[i]['symbol']
        except:
            symbol = ''
        try:
            price = d[i]['quote']['USD']['price']
        except:
            price = ''
        if i <= 99:
            try:
                trs = soup.find('div', class_='cmc-table__table-wrapper-outer').find('div').find_next('tbody').find_all(
                    'tr')
                link = f'https://coinmarketcap.com' + trs[i].find_all('td')[1].find('a', class_='cmc-link').get('href')
            except:
                link = ''
        elif i > 99:
            pattern += 1
            url2 = f'https://coinmarketcap.com/{pattern}/'
            html = get_url(url2)
            soup = BeautifulSoup(html, 'lxml')
            try:
                trs = soup.find('div', class_='cmc-table__table-wrapper-outer').find('div').find_next('tbody').find_all(
                    'tr')
                link = f'https://coinmarketcap.com' + trs[i - 100].find_all('td')[1].find('a', class_='cmc-link').get(
                    'href')
            except:
                link = ''
        count += 1
        print(count, id, name, symbol, price, link)


def main():
    url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=USD,BTC,ETH,XRP,BCH,' \
          'LTC&cryptocurrency_type=all&limit=200&sort=market_cap&sort_dir=desc&start=1'
    # url2 = 'https://coinmarketcap.com'
    pattern = 101
    count = 0
    while pattern < 2601:
        d = get_json(url)
        link_counter = 1
        get_data(d)
        url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=USD,BTC,ETH,XRP,BCH,' \
              'LTC&cryptocurrency_type=all&limit=200&sort=market_cap&sort_dir=desc&start=' + str(pattern)
        pattern += 200
        link_counter += 1
        global global_counter
        global_counter += 1
    print(count)


if __name__ == '__main__':
    main()

# print(gen_url(get_url('https://coinmarketcap.com')))
