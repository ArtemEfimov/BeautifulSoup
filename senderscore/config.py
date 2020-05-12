

"""for post request"""

cookies = {
    'ss_lookup': '8c1f71154ebf0ff660692ed68567ec13',
    'RPID': '5e49016b20e528.39787147',
    'driftt_aid': '18cf7106-e58b-4492-beff-915affcb77f4',
    'DFTT_END_USER_PREV_BOOTSTRAPPED': 'true',
    'driftt_sid': '9ce721c9-be19-427d-8b6b-19c8155ba1cb',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://senderscore.org',
    'Connection': 'keep-alive',
    'Referer': 'https://senderscore.org/',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

data = {
    'action': 'localLogin',
    'email': 'some@email.com',
    'password': 'password',
    'Submit': 'Sign in'
}
#--------------------------------------------------------------------------------------------------------------------

"""for post request after authorization"""


cookies1 = {
    'ss_lookup': '84524da22430ff0d9bf9665197390d8f',
    'RPID': '5e49016b20e528.39787147',
    'driftt_aid': '18cf7106-e58b-4492-beff-915affcb77f4',
    'DFTT_END_USER_PREV_BOOTSTRAPPED': 'true',
    'driftt_sid': 'f28446e2-fc4f-4608-911b-b90b856e38e5',
}



data1 = {
  'lookup': '14.169.220.138',
  'g-recaptcha-response': 'place for domain or ip'
}

























