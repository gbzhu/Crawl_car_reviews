from urllib import request
import json
import configparser
from crawler_src.db_manager import DBManger


def config_parser(filepath: str):
    cp = configparser.ConfigParser()
    cp.read(filenames=filepath, encoding='utf8')
    host = cp['mongodb']['host']
    port = cp['mongodb']['port']
    database = cp['mongodb']['database']
    target_website = cp['car_info']['target_website']
    makes = cp['car_info']['makes']
    pre_api = cp['car_info']['pre_api']
    suf_api = cp['car_info']['suf_api']
    pre_url = cp['car_info']['pre_url']
    return host, int(port), database, target_website, makes, pre_api, suf_api, pre_url


def joint_url(make: str, pre_api: str, suf_api: str):
    make = make.replace(' ', '-').lower()
    return pre_api + make + suf_api


def obtain_model_and_joint(db_manager: DBManger, makes: list, pre_api: str, suf_api: str, pre_url: str):
    for make in makes:

        print(make)

        make_url = joint_url(make=make, pre_api=pre_api, suf_api=suf_api)
        model_json = {}
        with request.urlopen(make_url) as resp:
            context = resp.read().decode('utf-8')
            json_obj = json.loads(context)
        data = json_obj['data']
        for model in data:
            detial_json = {}
            model_name = model['name']

            print(make + ':' + model_name)

            detial_json['description'] = model['description']
            detial_json['model_category'] = model['model_category']
            try:
                detial_json['primary_body_style'] = model['primary_body_style']
            except KeyError:
                pass
            detial_json['url'] = pre_url + model['url_slug']
            model_json[model_name] = detial_json
        db_manager.insert(col_name='car_urls', doc={'make': make, 'models': model_json})


if __name__ == '__main__':
    host, port, database, _, makes, pre_api, suf_api, pre_url = config_parser('../config.ini')
    makes = makes.split(',')
    db_manager = DBManger(host=host, port=port, db=database)
    obtain_model_and_joint(db_manager=db_manager, makes=makes, pre_api=pre_api, suf_api=suf_api, pre_url=pre_url)
