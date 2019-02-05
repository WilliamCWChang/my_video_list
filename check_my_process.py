import csv


def get_comic_list(filename):
    comic_list = []
    with open(filename, newline='', encoding='utf8') as csvfile:
        for row in csv.reader(csvfile):
            comic_list.append(
                {"unread": row[0],
                 "my_process": row[1],
                 "now_process": row[2],
                 "url": row[3],
                 "title": row[4],
                 })
    return comic_list


import requests
from bs4 import BeautifulSoup
import re


for comic in get_comic_list('my_anime1_list.csv'):
    r = requests.get(comic["url"])
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.main.h2.find_all('a')[0].text

    print(comic["title"] + " now is " + data)
