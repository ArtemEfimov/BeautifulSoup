
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
    r = s.split(' ')[0]
    return r.replace(',', '')


def write_csv(data):
    with open('plugins4.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'],
                         data['url'],
                         data['reviews']))


def write_row(row):
    with open('plugins5.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([row])


def get_block_name(html):
    soup = BeautifulSoup(html, 'lxml')
    main_page_of_the_plugin_group = soup.find('main', id='main')
    group = main_page_of_the_plugin_group.find('h1', class_='page-title').find('strong').text
    write_row(group)

def get_plugin_data(html):
    soup = BeautifulSoup(html, 'lxml')
    all_plugins = soup.find('main', id='main').find_all('article')
    for plugin in all_plugins:
        name = plugin.find('h2').find('a').text
        url = plugin.find('h2').find('a').get('href')
        r = plugin.find('span', class_='rating-count').find('a').text
        rating = refined(r)

        data = {
            'name': name,
            'url': url,
            'reviews': rating}

        write_csv(data)

def main():
    pattern = 'https://wordpress.org/plugins/browse/{}/'
    plugin_list = ['blocks', 'featured', 'beta', 'popular']
    for i in plugin_list:
        url = pattern.format(i)
        # url = f'https://wordpress.org/plugins/browse/{i}/'
        html = get_html(url)
        get_block_name(html)

        while True:
            soup = BeautifulSoup(get_html(url), 'lxml')
            try:
                pattern1 = 'Next'
                url = soup.find('a', class_='next page-numbers', text=re.compile(pattern1)).get('href')
                html = get_html(url)
                get_plugin_data(html)
            except:
                break
        get_plugin_data(html)


if __name__ == '__main__':
    main()
