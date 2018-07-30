from urllib import request
import json
import configparser
from crawler_src.db_manager import DBManger

makes = ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'BMW', 'Bentley', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet',
         'Chrysler', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar',
         'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda',
         'McLaren', 'Mercedes-AMG', 'Mercedes-Benz', 'Mercedes-Maybach', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani',
         'Polestar', 'Porsche', 'Ram', 'Rolls-Royce', 'Scion', 'Smart', 'Spyker', 'Subaru', 'Tesla', 'Toyota',
         'Volkswagen', 'Volvo']

pre_url = 'https://www.caranddriver.com/list-reviews-in-depth'


def joint_url(make: str):
    make = make.replace(' ', '-').lower()
    return 'https://api-prod.caranddriver.com/v1/models/make/' + make + '?is_hidden=false&is_in_navigation=true'


def obtain_model_and_joint(db_manager: DBManger):
    for make in makes:

        print(make)

        make_url = joint_url(make=make)
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
    cp = configparser.ConfigParser()
    cp.read(filenames='../config.ini', encoding='utf8')
    host = cp['mongodb']['host']
    port = cp['mongodb']['port']
    database = cp['mongodb']['database']
    db_manager = DBManger(host=host, port=int(port), db=database)
    obtain_model_and_joint(db_manager=db_manager)
