import requests
from pprint import pprint
from urllib.parse import urlparse

# url='https://api-ssl.bitly.com/v4/user'
# headers = {'Authorization': 'Bearer b77c507cb2b6226905f939f69b020009488aca14'}
# response = requests.get(url,headers=headers)
# response.raise_for_status()
# pprint(response.json())
#
# endpoint_bitlinks = 'https://api-ssl.bitly.com/v4/bitlinks'
endpoint_count_links = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
# endpoint_bitlink_info = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
# token = 'Bearer b77c507cb2b6226905f939f69b020009488aca14'


# def parsed_link(url):
#     url_parsed = urlparse(url)
#     print(url_parsed._replace(scheme='').geturl())
#     return url_parsed._replace(scheme='').geturl()
#
#
# def shorten_link(token, url):
#     payload = {'long_url': url}
#     headers = {'Authorization': token}
#     response = requests.post(endpoint_bitlinks, headers=headers, json=payload)
#     response.raise_for_status()
#     return response.json()['link']
#
#
# def count_clicks(token, url):
#     headers = {'Authorization': token}
#     url_bitlink = endpoint_count_links.format(bitlink=url)
#     response = requests.get(url_bitlink, headers=headers)
#     response.raise_for_status()
#     return response.json()['total_clicks']
#
#
# def is_bitlink(url):
#     headers = {'Authorization': token}
#     url_bitlink_info = endpoint_bitlink_info.format(bitlink=url)
#     response = requests.get(url_bitlink_info, headers=headers)
#     return response.ok
#
#
# if __name__ == '__main__':
#     user_url = input('Введите ссылку: ')
#     if not is_bitlink(parsed_link(user_url)):
#         try:
#             print('Битлинк', shorten_link(token, user_url))
#         except requests.exceptions.HTTPError as e:
#             print(f'Произошла ошибка: {e}')
#     else:
#         try:
#             print('Количество кликов', count_clicks(token, parsed_link(user_url)))
#         except requests.exceptions.HTTPError as e:
#             print(f'Произошла ошибка: {e}')

# locations = ['Лондон', 'Аэропорт Шереметьево', 'Череповец']
# url = 'https://wttr.in/{}'
# payload = {'Tqmn3': '', 'lang': 'ru'}
# for location in locations:
#     url_template = url.format(location)
#     response = requests.get(url_template, params=payload)
#     response.raise_for_status()
#     print(response.text)

# import time
# import curses
# import asyncio
#
#
# def draw(canvas):
#     row, column = (1, 1)
#     row1, column1 = (1, 3)
#     row2, column2 = (1, 5)
#     curses.curs_set(False)
#     canvas.border()
#     coroutine = blink(canvas, row, column)
#     coroutine1 = blink(canvas, row1, column1)
#     coroutine2 = blink(canvas, row2, column2)
#     coroutines = [coroutine, coroutine1, coroutine2]
#     while True:
#         for coroutine in coroutines.copy():
#             try:
#                 coroutine.send(None)
#                 canvas.refresh()
#             except StopIteration:
#                 coroutines.remove(coroutine)
#             if len(coroutines) == 0:
#                 break
#
#
# async def blink(canvas, row, column, symbol='*'):
#     while True:
#         canvas.addstr(row, column, symbol, curses.A_DIM)
#         await asyncio.sleep(0)
#
#         canvas.addstr(row, column, symbol)
#         await asyncio.sleep(0)
#
#         canvas.addstr(row, column, symbol, curses.A_BOLD)
#         await asyncio.sleep(0)
#
#         canvas.addstr(row, column, symbol)
#         await asyncio.sleep(0)
#
#
# if __name__ == '__main__':
#     curses.update_lines_cols()
#     curses.wrapper(draw)

from time import sleep
import curses
import asyncio
from random import randint
from random import choice


async def blink(canvas, row, column, symbol='*', delay=1):
    for _ in range(delay):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(20):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(5):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)
            canvas.refresh()


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw(canvas):
    window = curses.initscr()
    max_row, max_column = window.getmaxyx()
    curses.curs_set(False)
    canvas.border()
    stars_type = ['+', '*', '.', ':']
    coroutines_stars = [blink(canvas, randint(1, max_row - 5), randint(1, max_column - 5),
                              choice(stars_type), randint(0, 30)) for _ in range(30)]
    coroutine_shot = fire(canvas, round(max_row / 2), round(max_column / 2))
    coroutines_stars.append(coroutine_shot)

    while True:
        for coroutine in coroutines_stars.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines_stars.remove(coroutine)
            if len(coroutines_stars) == 0:
                break
        sleep(0.1)


if __name__ == '__main__':

    curses.update_lines_cols()
    curses.wrapper(draw)
