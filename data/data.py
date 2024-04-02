import os
import json
import csv
from urllib.parse import quote, quote_plus
from sqlalchemy import create_engine, MetaData, Table, select, text
from urllib.parse import quote_plus

password = "P@ssw0rd!"
host = "127.0.0.1"
port = "3306"
database = "cramschool"

encoded_password = quote_plus(password)
connection_string = f"mariadb://root:{encoded_password}@{host}:{port}/{database}?charset=utf8"
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(bind=engine)

def get_cramschool_common_city_id():
    with engine.connect() as conn:
        sql = text('select * from cramschool_common_city')
        result = conn.execute(sql)
        return [{row[1]: row[0]} for row in result]


def get_cramschool_common_category_id():
    with engine.connect() as conn:
        sql = text('select * from cramschool_common_category')
        result = conn.execute(sql)
        return [{row[1]: row[0]} for row in result]


def get_cramschool_info_id():
    with engine.connect() as conn:
        sql = text('select * from cramschool_management_info')
        result = conn.execute(sql)
        return [{row[1]: row[0]} for row in result]


def transformer_info_data():
    csvResult = []
    cities = get_cramschool_common_city_id()
    categories = get_cramschool_common_category_id()

    files = os.listdir('.')
    json_files = [file for file in files if file.endswith('.json')]

    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)

        for afterschool in data:
            if '主管機關文件單位代碼' in afterschool:
                del afterschool['主管機關文件單位代碼']
            if '各地短期補習班數量' in afterschool:
                del afterschool['各地短期補習班數量']
            if '短期補習班類別' in afterschool:
                del afterschool['短期補習班類別']

            for city_info in cities:
                city_name = next(iter(city_info.keys()))
                if afterschool['地區縣市'] == city_name:
                    afterschool['地區縣市'] = city_info[city_name]

            csvResult.append(afterschool)

    return csvResult, cities, categories

def cramschool_category():
    infos = get_cramschool_info_id()
    csvResult = []
    cities = get_cramschool_common_city_id()
    categories = get_cramschool_common_category_id()

    files = os.listdir('.')
    json_files = [file for file in files if file.endswith('.json')]

    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)

        for afterschool in data:
            keys_to_keep = ['短期補習班名稱', '短期補習班類別']
            afterschool = {key: value for key,
                           value in afterschool.items() if key in keys_to_keep}

            for category in afterschool['短期補習班類別'].split('、'):
                new_afterschool = afterschool.copy()
                new_afterschool['短期補習班類別'] = category
                for category_info in categories:
                    category_name = next(iter(category_info.keys()))
                    if category == category_name:
                        new_afterschool['短期補習班類別'] = category_info[category_name]

                csvResult.append(new_afterschool)

    for info in infos:
        info_name = next(iter(info.keys()))
        for item in csvResult:
            if item['短期補習班名稱'] == info_name:
                item['短期補習班名稱'] = info[info_name]

    return csvResult

def cramschool_info_csv():
    csvResult, cities, categories = transformer_info_data()
    csv_file = 'data.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for item in csvResult:
            print(item)
            row = [str(value) for value in item.values()]
            writer.writerow(row)

    print('data.csv is created')
    print(cities)
    print(categories)


def cramschool_category_csv():
    csvResult = cramschool_category()
    csv_file = 'cramschool_category.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for item in csvResult:
            print(item)
            row = [str(value) for value in item.values()]
            writer.writerow(row)

    print('cramschool_category.csv is created')


cramschool_info_csv()
cramschool_category_csv()
