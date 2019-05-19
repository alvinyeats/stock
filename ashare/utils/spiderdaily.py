import re
import datetime
import time

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

from ashare.models import AShare, AShareDaily


URL = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240541747953776514_1558258694304&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p=0&ps=20&_=1558258694412'


def get_one_page(i):
    try:
        print(i)
        url = URL.replace('p=0', 'p={}'.format(i))
        print(url)
        res = requests.get(url)
        if res.status_code == 200:
            text = res.text[41:-1].replace('data', '"data"')
            text = re.sub(r"\,recordsFiltered\:\d+", "", text)
            return text
        return None
    except requests.RequestException:
        print('crawl failed')


def write_to_db(tbl):
    data = json.loads(tbl)
    today = datetime.date.today()
    if today.weekday() >= 5:
        dd = today.weekday() - 4
        today = today - datetime.timedelta(days=dd)

    for sd in data['data']:
        try:
            sd = sd.split(',')
            stock = AShare.objects.get(no=sd[1])
            AShareDaily.objects.create(
                stock=stock,
                today=today,
                price_open=sd[12],
                price_close=sd[13],
                price_upper=sd[10],
                price_lower=sd[11],
                rise_rate=sd[5],
                rise_amt=sd[6]
            )
            print('saving {}'.format(stock.no))
        except:
            print('already exist')


def spider_daily(page):
    for i in range(1, page):
        html = get_one_page(i)
        write_to_db(html)
        time.sleep(1)


if __name__ == '__main__':
    spider_daily(3)