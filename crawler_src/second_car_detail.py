from crawler_src.db_manager import DBManger
from crawler_src.fisrt_car_list import config_parser
from urllib import request
from bs4 import BeautifulSoup


def get_review(url: str):
    with request.urlopen(url) as resp:
        context = resp.read().decode('utf8')
        bs4_obj = BeautifulSoup(context, 'html5lib')
        # this can get all result
        href_a_tags = bs4_obj.find_all('a', class_='gtm-link gtm-article-title')
        text_p_tags = bs4_obj.find_all('p', class_='col-24 serif-2 f18 lh22 text-nero mb4 mb5-dk')
        for index in range(len(href_a_tags)):
            href = href_a_tags[index]['href']
            title = href_a_tags[index].get_text()
            description = text_p_tags[index].get_text()

        print(1)


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
