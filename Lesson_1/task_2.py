"""
2. Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент
для города, название которого получается через input. https://openweathermap.org/current
"""

import configparser
import requests
from pprint import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["OpenWeather"]["api_key"]


def current_weather(city):
    url = f' http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    r = requests.get(url, headers=headers)
    return r.json()


city_weather = input('Введите город для получения текущей погоды: ')
result = current_weather(city_weather)
pprint(result)
