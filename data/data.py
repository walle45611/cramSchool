import os
import json
import csv
import re
from urllib.parse import quote, quote_plus
from sqlalchemy import create_engine, MetaData, Table, select,text
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
        return [{row[1]:row[0]} for row in result]

def get_cramschool_management_category_id():
    with engine.connect() as conn:
        sql = text('select * from cramschool_management_category')
        result = conn.execute(sql)
        return [{row[1]:row[0]} for row in result]

def transformer_data():
    csvResult = []
    cities = get_cramschool_common_city_id()
    categories = get_cramschool_management_category_id()

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

            for city_info in cities:
                city_name = next(iter(city_info.keys()))  
                if afterschool['地區縣市'] == city_name:
                    afterschool['地區縣市'] = city_info[city_name]        

            for category in afterschool['短期補習班類別'].split('、'):
                new_afterschool = afterschool.copy()
                new_afterschool['短期補習班類別'] = category
                for category_info in categories:
                    category_name = next(iter(category_info.keys()))
                    if category == category_name:
                        new_afterschool['短期補習班類別'] = category_info[category_name]

                csvResult.append(new_afterschool)


    return csvResult, cities, categories

def data_csv():
    csvResult,cities,categories = transformer_data()
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

data_csv()