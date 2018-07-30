from crawler_src.db_manager import DBManger
from crawler_src.fisrt_car_list import config_parser
from urllib import request
from bs4 import BeautifulSoup


def get_review(url: str):
    with request.urlopen(url) as resp:
        context = resp.read().decode('utf8')
        bs4_obj = BeautifulSoup(context, 'html5lib')
        # this can get all result
        a_tag = bs4_obj.find_all('a', class_='gtm-link gtm-article-title')


if __name__ == '__main__':
    host, port, database, makes, pre_api, suf_api, pre_url = config_parser('../config.ini')
    db_manager = DBManger(host, port, database)
    res = db_manager.find_all(col_name='car_urls')
    for re in res:
        make = re['make']
        models = re['models']
        for model in models:
            url = models[model]['url']
            get_review(url)
