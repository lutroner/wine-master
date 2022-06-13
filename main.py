from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
drinks_dataset = read_excel('wine.xlsx', sheet_name='Лист1')
foundation_date = datetime(year=1920, month=1, day=1)
drinks = drinks_dataset.to_dict(orient='records')
drinks_categories = list(dict.fromkeys(drinks_dataset['Категория'].to_list()))

# Избавляемся от non в значениях словаря
for drink in drinks:
    for key, item in drink.items():
        if str(drink[key]) == 'nan':
            drink[key] = ''

rendered_page = template.render(
    current_time=f'Уже {datetime.now().year - foundation_date.year} года с вами',
    # Преобразуем словарь в новый с категориями в качестве ключей
    wine_category_list={category: [drink for drink in drinks
                                   if drink['Категория'] == category]
                        for category in drinks_categories}
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
