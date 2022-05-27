from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
wine_data = read_excel('wine.xlsx', sheet_name='Лист1',
                       usecols=['Картинка', 'Категория', 'Название',
                                'Сорт', 'Цена', 'Акция'])
open_date = datetime(year=1920, month=1, day=1)
wine_dict = wine_data.to_dict(orient='records')
category_list = list(dict.fromkeys(wine_data['Категория'].to_list()))

# Избавляемся от non в значениях словаря
for di in wine_dict:
    for key, item in di.items():
        if str(di[key]) == 'nan':
            di[key] = ''

rendered_page = template.render(
    current_time=f'Уже {datetime.now().year - open_date.year} года с вами',
    # Преобразуем словарь в новый с категориями в качестве ключей
    wine_category_list={category: [wine for wine in wine_dict
                                   if wine['Категория'] == category]
                        for category in category_list}
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
