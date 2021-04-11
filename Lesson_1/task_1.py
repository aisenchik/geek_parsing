"""
Задание

1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

"""

import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}


def list_repos(username):
    my_repos = []
    url = f'https://api.github.com/users/{username}/repos'
    r = requests.get(url, headers=headers)
    with open('my_repos.json', 'w') as outfile:
        json.dump(json.loads(r.text), outfile)

    with open('my_repos.json', 'r') as outfile:
        for dict_json in json.load(outfile):
            my_repos.append(dict_json['full_name'])
    return my_repos


print(list_repos(username='aisenchik'))
