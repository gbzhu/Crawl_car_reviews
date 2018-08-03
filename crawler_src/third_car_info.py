from crawler_src.db_manager import DBManger
from crawler_src.fisrt_car_list import config_parser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError


def obtain_car_info(url: str, target_website: str):
    reviews = {}
    try:
        with urlopen(url) as resp:
            context = resp.read().decode('utf-8')
    except HTTPError as e:
        print(e.msg)
        return None
    bs4_obj = BeautifulSoup(context, 'lxml')
    ng_parent = bs4_obj.find('div',
                             class_='w100p w180-dk w300-tb hauto border-top-dotted-tb border-gainsboro pb1 pt4-tb block mt4 mt2-dk mb5-dk hide-tb ph20 ph0-nm mr8-dk')
    try:
        ngs = ng_parent.find_all('a', class_='gtm-link gtm-article-page')
    except AttributeError as e:
        print(e)
        return None
    ng_url = {}
    ng_order = []
    for ng_tag in ngs:
        href = ng_tag['href']
        href = target_website + href
        ng = str(ng_tag.get_text()).replace('\n', '').strip()
        ng_order.append(ng)
        ng_url[ng] = href

    for ng in ng_order:
        if 'Overview' in ng:
            ng_info = obtain_ng_info(bs4_obj)
        else:
            try:
                with urlopen(ng_url[ng]) as resp_2:
                    context_2 = resp_2.read().decode('utf-8')
            except:
                continue
            bs4_obj_2 = BeautifulSoup(context_2, 'lxml')
            ng_info = obtain_ng_info(bs4_obj_2)
        reviews[ng] = ng_info
    return reviews


def obtain_ng_info(bs4_obj: BeautifulSoup):
    title_info = []
    div_tag = bs4_obj.find('div',
                           class_='embedded-article-article flex-grow mb6-nm mb4 f16 f18-dk lh25 lh28-tb lh30-dk serif text-nero ph20 ph0-nm')

    div_title_tag = div_tag.contents
    index = 0
    title, info = '', ''
    while index < len(div_title_tag):

        h3_tag = div_title_tag[index].find('h3')
        p_tag = div_title_tag[index].find('p')
        if h3_tag is not None:
            title = h3_tag.get_text().replace('\n', '').strip()
            if p_tag is None:
                pass
            else:
                info = p_tag.get_text().replace('\n', '').strip()
        else:
            if p_tag is None or p_tag.get_text() == '':
                index += 1
                continue
            else:
                info += p_tag.get_text().replace('\n', '').strip()
        flag = True
        for num in range(len(title_info)):
            if title in title_info[num].keys():
                title_info[num] = {title: info}
                flag = False
                break
        if flag:
            title_info.append({title: info})

        index += 1
    return title_info


if __name__ == '__main__':
    host, port, database, target_website, _, pre_api, suf_api, pre_url = config_parser('../config.ini')
    db_manager = DBManger(host, port, database)
    car_details = db_manager.find_by_condition(col_name='car_details', condition={'flag': 'false'})
    for car_detail in car_details:
        make_model = car_detail['make_model']

        cars = car_detail['cars']
        finish_url = []
        for car in cars:
            for key, value in car.items():
                brand = key

                print(make_model + " : " + brand)

                href = value['href']
                if 'page' in href:
                    href = href.split('-review-')[0] + '-review'
                    brand = href.split('/reviews/')[1].split('-in-depth-model-')[0]

                    print(make_model + " : " + brand)

                if href in finish_url:
                    print("it's finished")
                    continue
                reviews = obtain_car_info(href, 'https://www.caranddriver.com')
                finish_url.append(href)
                if reviews is None:
                    continue
                reviews['car_info'] = make_model + " / " + brand
                db_manager.insert(col_name='car_reviews', doc=reviews, check_keys=False)
        db_manager.update(col_name='car_details', query={'make_model': make_model}, update={'$set': {'flag': 'true'}})
