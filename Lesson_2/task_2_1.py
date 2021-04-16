"""
Вариант 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
"""

import json
import time
import numpy as np
import pandas as pd
import time
import pickle
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs

main_url = "https://hh.ru"


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get(url, headers, params, proxies):
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return r


def hh_page_parse(soup, url):
    items = soup.find_all("div", attrs={"class": ["vacancy-serp-item", "vacancy-serp-item_premium"]})
    items_info = []

    for item in items:
        min_price = None
        max_price = None
        info = {}
        a = item.find("a", attrs={"class": "bloko-link"})
        price = item.find("div", attrs={"class": "vacancy-serp-item__sidebar"}).text.replace("\u202f", "")
        if 'руб' in price:
            price = price.replace('руб.', '').strip()
        if 'от' in price:
            min_price = price.replace('от', '').strip()
        elif 'до' in price:
            max_price = price.replace('до', '').strip()
        if '-' in price:
            min_price, max_price = price.split('–')
        info['href'] = a.attrs["href"]
        info["name"] = a.text
        if min_price:
            info["min_price"] = float(min_price)
        else:
            info["min_price"] = np.NaN
        if max_price:
            info["max_price"] = float(max_price)
        else:
            info["max_price"] = np.NaN
        # info["price"] = price
        info["company"] = item.find("a", attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text.replace("\xa0", " ")
        info["link_page"] = url
        items_info.append(info)
    return pd.DataFrame.from_records(items_info)


vacancy = input('Введите должность: ')
url = f"https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={vacancy}"
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Safari/537.36"
}
proxies = {
    'http': '213.108.18.34'
}

params = {

}

r = get(url, headers, params, proxies)

path = "hh.main"
# save_pickle(r, path)
# with open("vacancies.json", "w") as f:
#     json.dump(items_info, f, indent=2, ensure_ascii=False)
# r = load_pickle(path)

page = bs(r.text, "html.parser")
try:
    next_page = page.find("a", attrs={"data-qa": "pager-next"})
except Exception as e:
    print(e)

result = pd.DataFrame()
if next_page:
    while next_page:
        print(f"Обработка ссылки: {url}")
        res = hh_page_parse(page, url)
        url = main_url + next_page.attrs["href"]
        try:
            next_page = page.find("a", attrs={"data-qa": "pager-next"})
        except Exception as e:
            print(e)
            break
        result = pd.concat([result, res])
        time.sleep(1)
        r = get(url, headers, params, proxies)
        page = bs(r.text, "html.parser")
else:
    result = hh_page_parse(page, url)

result.to_csv("result.csv", index=False)
