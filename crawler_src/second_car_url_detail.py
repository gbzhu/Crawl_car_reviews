from db_manager.db_manager import DBManger
from crawler_src.fisrt_car_list import config_parser
from urllib import request
from urllib import error
from bs4 import BeautifulSoup

finish = ['Chrysler', 'Ford', 'Mitsubishi', 'Subaru', 'Tesla', 'Acura', 'Alfa Romeo']


def get_review(make_model: str, url: str, target_website: str, db_manager: DBManger):
    print(make_model)
    try:
        with request.urlopen(url) as resp:
            context = resp.read().decode('utf8')
    except error.HTTPError as e:
        print(e.msg)
        return
    bs4_obj = BeautifulSoup(context, 'html5lib')
    # this can get all result
    href_a_tags = bs4_obj.find_all('a', class_='gtm-link gtm-article-title')
    text_p_tags = bs4_obj.find_all('p', class_='col-24 serif-2 f18 lh22 text-nero mb4 mb5-dk')
    for index in range(len(href_a_tags)):
        href = href_a_tags[index]['href']
        href = target_website + href
        title = href_a_tags[index].get_text()

        print(make_model + " : " + title)

        description = text_p_tags[index].get_text()
        db_manager.update(col_name='car_details', query={'make_model': make_model}, update={'$addToSet': {
            'cars': {title: {'description': description, 'href': href}}}}, upsert=True)


if __name__ == '__main__':
    host, port, database, target_website, _, pre_api, suf_api, pre_url = config_parser('../config.ini')
    db_manager = DBManger(host, port, database)
    res = db_manager.find_all(col_name='car_urls')
    for re in res:
        make = re['make']
        if make in finish:
            print(make + ': continue')
            continue
        models = re['models']
        for model in models:
            url = models[model]['url']
            get_review(make + ' / ' + model, url, target_website, db_manager)
