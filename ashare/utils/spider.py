import requests
import pandas as pd
from bs4 import BeautifulSoup

from ashare.models import AShare


URL = 'http://s.askci.com/stock/a/?'


def get_one_page(i):
    try:
        args = {
            'reportTime': '2019-05-19',
            'pageNum': i
        }
        res = requests.get(URL, params=args)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        print('crawl failed')


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select('#myTable04')[0]  # [0]将返回的list改为bs4类型
    tbl = pd.read_html(content.prettify(), header=0)[0]
    # prettify()优化代码,[0]从pd.read_html返回的list中提取出DataFrame

    tbl.rename(columns={'股票代码':'no', '股票简称':'abbr', '公司名称':'company_name', '省份':'province', '城市':'city', '主营业务收入(201712)':'main_bussiness_income', '净利润(201712)':'net_profit', '员工人数':'employees', '上市日期':'listing_date', '招股书':'zhaogushu', '公司财报':'financial_report', '行业分类':'industry', '产品类型':'industry_type', '主营业务':'main_business'},inplace = True)

    print(tbl.no)
    return tbl
    # rename将表格15列的中文名改为英文名，便于存储到mysql及后期进行数据分析
    # tbl = pd.DataFrame(tbl,dtype = 'object') #dtype可统一修改列格式为文本


def write_to_db(tbl):
    for stock in tbl.itertuples():
        try:
            AShare.objects.create(
                no=str(stock.no).zfill(6),
                abbr=stock.abbr,
                industry=stock.industry,
            )
            print('saving {}'.format(stock.no))
        except:
            print('already exist')


def spider_main(page):
    for i in range(1, page):
        html = get_one_page(i)
        stocks = parse_one_page(html)
        write_to_db(stocks)


if __name__ == '__main__':
    spider_main(4)