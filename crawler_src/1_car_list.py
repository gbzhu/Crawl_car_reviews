from urllib import request
import json

makes = ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'BMW', 'Bentley', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet',
         'Chrysler', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'GMC', 'Genesis', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar',
         'Jeep', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda',
         'McLaren', 'Mercedes-AMG', 'Mercedes-Benz', 'Mercedes-Maybach', 'Mini', 'Mitsubishi', 'Nissan', 'Pagani',
         'Polestar', 'Porsche', 'Ram', 'Rolls-Royce', 'Scion', 'Smart', 'Spyker', 'Subaru', 'Tesla', 'Toyota',
         'Volkswagen', 'Volvo']


def joint_url(make: str):
    make = make.replace(' ', '-').lower()
    return 'https://api-prod.caranddriver.com/v1/models/make/' + make + '?is_hidden=false&is_in_navigation=true'


def obtain_model_and_joint():
    for make in makes:
        make_url = joint_url(make=make)
        with request.urlopen(make_url) as resp:
            context = resp.read().decode('utf-8')
            json_obj = json.loads(context)
            data = json_obj['data']
            for model in data:
                description = model['description']
                model_category = model['model_category']
                primary_body_style = model['primary_body_style']
                url_slug = model['url_slug']


if __name__ == '__main__':
    obtain_model_and_joint()
