import csv
import logging
from collections import namedtuple
from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool
from time import sleep
#.prettify())
logging.basicConfig(level='DEBUG')
logger = logging.getLogger('Etp')

ParseResult = namedtuple(
    'ParseResult',
    (
        'auction_code',
        'name_subject',
        'deadline',
        'holding_an_auction',
        'status',
    )

)

HEADERS = ('Код аукциона',
           'Наименование субъекта закупки',
           'Окончание срока подачи',
           'Проведение аукциона',
           'Статус'
           )


class EtpEtsParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
                                'Accept - Language': 'ru'

                                }
        self.result = []

    def write_scv(self):
        with open('test.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

    def load_page(self, url: str):
        # url = 'https://www.etp-ets.ru/procedure/catalog/?page=1&limit=25'
        res = self.session.get(url=url)
        if res.ok:
            return res.text
        while not res.ok:
            sleep(2)
            res = self.session.get(url=url)
        return res.text



    def parse_page(self, text: str):
        soup = BeautifulSoup(text, 'lxml')
        trs = soup.find('table', class_='mte-grid-table table table-bordered table-striped table-hover').find(
            'tbody').find_all('tr')
        if not trs:
            logger.error('no trs')
            return
        for tr in trs:
            self.store_data(tr)

    def store_data(self, tr):
        auction_code = tr.find_all('td')[1].text.split()[-1]
        if not auction_code:
            logger.error('no auction code')
        name_subject = tr.find_all('td')[1].text.strip().replace('\n', ' ').split('(')[0]
        if not name_subject:
            logger.error('no name subject')
        deadline = tr.find_all('td')[5].text.strip().replace('\n', '')
        if not deadline:
            logger.error('deadline')
        holding_an_auction = tr.find_all('td')[-3].text.strip().replace('\n', 'n')
        if not holding_an_auction:
            logger.error('no holding an auction')
        status = tr.find_all('td')[-2].text.strip().replace('\n', 'n')
        if not status:
            logger.error('no status')
        self.result.append(
            ParseResult
                (
                auction_code=auction_code,
                name_subject=name_subject,
                deadline=deadline,
                holding_an_auction=holding_an_auction,
                status=status,
            )
        )

    def make_all(self, url):
        text = self.load_page(url)
        self.parse_page(text=text)

    def run(self):
        urls = [f'https://www.etp-ets.ru/procedure/catalog/?page={i}&limit=25' for i in range(1, 17779)]
        logger.info(f'{urls}')
        with Pool(40) as p:
            p.map(self.make_all, urls)
        # for url in urls:
        #     self.make_all(url)
        self.write_scv()
        logger.info(f'Получено результатов: {len(self.result)}. Парсер завершил сбор данных')


if __name__ == '__main__':
    parser = EtpEtsParser()
    parser.run()
