from crawler_src.db_manager import DBManger
from crawler_src.fisrt_car_list import config_parser
from urllib.request import urlopen
from bs4 import BeautifulSoup


def obtain_car_info(url: str, target_website: str):
    ng_review = {}
    finish_url = []
    if url[-6:] != 'review':
        url = url.split('-review-')[0] + '-review'
    if url in finish_url:
        return
    ng_url = {}
    with urlopen(url) as resp:
        context = resp.read().decode('utf-8')
    bs4_obj = BeautifulSoup(context, 'lxml')

    ov_tag = bs4_obj.find('div',
                          class_='embedded-article-article flex-grow mb6-nm mb4 f16 f18-dk lh25 lh28-tb lh30-dk serif text-nero ph20 ph0-nm')
    overview = []
    title, detail = [], []
    h3_tags = ov_tag.find_all('h3')
    p_tags = ov_tag.find_all('p')
    for h3_tag in h3_tags:
        h3 = h3_tag.get_text().replace('\n', '').strip()
        title.append(h3)
    p_info = ''
    for p_tag in p_tags:
        p = p_tag.get_text().replace('\n', '').strip()
        p_info += p
        if p == '' and p_info not in detail:
            detail.append(p_info)
            p_info = ''
    for index in range(len(title)):
        overview.append({title[index]: detail[index]})

    ng_parent = bs4_obj.find('div',
                             class_='w100p w180-dk w300-tb hauto border-top-dotted-tb border-gainsboro pb1 pt4-tb block mt4 mt2-dk mb5-dk hide-tb ph20 ph0-nm mr8-dk')

    ngs = ng_parent.find_all('a', class_='gtm-link gtm-article-page')
    for ng_tag in ngs:
        href = ng_tag['href']
        href = target_website + href
        ng = str(ng_tag.get_text()).replace('\n', '').strip()
        ng_url[ng] = href

    for key, value in ng_url:
        if key == 'Overview':
            continue
        ng_info = obtain_ng_info(ng_url=value)

    finish_url.append(url)


def obtain_ng_info(ng_url: str):
    """
    obtain info of special ng
    :param ng_url:
    :return: a list contains json info
    """
    ret_detail = []

    with urlopen(url) as resp:
        context = resp.read().decode('utf-8')
    bs4_obj = BeautifulSoup(context, 'lxml')

    div_tag = bs4_obj.find('div',
                           class_='embedded-article-article flex-grow mb6-nm mb4 f16 f18-dk lh25 lh28-tb lh30-dk serif text-nero ph20 ph0-nm')

    div_title_tag = div_tag.children
    index = 0
    while index < len(div_title_tag):
        h3_tags = div_title_tag[index].find('h3')
        p_tag = div_title_tag[index].find('p')

    return 1


if __name__ == '__main__':

    # host, port, database, target_website, _, pre_api, suf_api, pre_url = config_parser('../config.ini')
    # db_manager = DBManger(host, port, database)
    url = 'https://www.caranddriver.com/reviews/2018-acura-nsx-in-depth-model-review'
    obtain_car_info(url, 'https://www.caranddriver.com')
