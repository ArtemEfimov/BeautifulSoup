import csv
import logging
import re
from collections import namedtuple
import requests
from config import headers, cookies, data, data1
from bs4 import BeautifulSoup
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('Sender_score')

HEADERS = ('ip ',
           'senderscore',
           'hostname',
           'domain',
           )

ParseResult = namedtuple(
    'ParseResult',
    (
        'ip',
        'senderscore',
        'hostname',
        'domain',
    )

)


# def get_authorization():
#     """ Attempt to sign in"""
#     s = requests.Session()
#     response = s.post('https://senderscore.org/', headers=headers, cookies=cookies,
#                       data=data)  # вот это все для авторизации тут ок
#     if response.status_code == 200:
#         print(response.headers)
#         return response.url
#     return logger.error("access denied!!!")


def send_ip(url):
    """ Attempt to send ip and get data"""
    logger.info(f'url after authorization: {url} ')
    api_key = 'api_key'
    site_key = '6Ldl3RoUAAAAAIRdHJ0QcZNaTdOeUpnE4_p1SaEV'  # grab from site
    client = AnticaptchaClient(api_key)
    task = NoCaptchaTaskProxylessTask(url, site_key)
    job = client.createTask(task)
    job.join()
    solution = job.get_solution_response()
    data1['g-recaptcha-response'] = solution
    s = requests.Session()
    response = s.post('https://senderscore.org/recaptcha.php', headers=headers, cookies=cookies, data=data1)
    logger.info("Processed successfully")
    logger.info(
        f'second URL is: {response.url}')  # https://senderscore.org/lookup.php?lookup=14.169.220.128&validLookup=true
    return response.text


def get_page_data(response: str) -> list:
    result = []
    soup = BeautifulSoup(response, 'lxml')
    start_with = soup.find('h3', class_='text-center').find('strong').text.strip()
    metric = soup.find('form', id='mktoForm_1088').find_next_sibling().text
    met = re.search(r'"sSORGScore":"\d+"', metric).group().split(':')[-1].replace('"', "")
    host = soup.find('th', scope='row').find_next_sibling().text.strip()
    trs = soup.find('table',
                    class_="table table-sm table-sortable table-fixed table-striped table-hover table-responsive-md") \
        .find('tbody', class_="").find_all('tr')
    for tr in trs:
        ip = start_with
        senderscore = met
        hostname = host
        domain = tr.find('a').text.strip()
        result.append(ParseResult
            (
            ip=ip,
            senderscore=senderscore,
            hostname=hostname,
            domain=domain,
        ))
    return result


def write_csv(result: list):
    with open('test2.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for item in result:
            writer.writerow(item)


if __name__ == '__main__':
    # url = get_authorization()
    url = 'https://senderscore.org/'
    result = send_ip(url)
    parse_list = get_page_data(result)
    write_csv(parse_list)
