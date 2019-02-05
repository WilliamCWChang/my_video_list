import csv
import requests
from bs4 import BeautifulSoup


def get_comic_list_from_csv(csvfilename):
    comic_list = []
    with open(filename, newline='', encoding='utf8') as csvfile:
        for row in csv.reader(csvfile):
            if len(row) < 3:
                continue
            comic_list.append(
                {
                    "my_process": row[1],
                    "url": row[3],
                })
    return comic_list


def set_comic_list_to_csv(filename, comic_list):
    with open(filename, newline='', encoding='utf8', mode='w') as csvfile:
        data_list = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for comic in comic_list:
            data_list.writerow(comic)
            print(comic)


filename = 'Readme.md'

set_comic_list = []
for comic in get_comic_list_from_csv(filename):

    r = requests.get(comic["url"])
    soup = BeautifulSoup(r.text, 'html.parser')

    if "近期文章" in soup.main.h2.text:
        print("The page is not found. url={}".format(comic["url"]))
        continue

    print(soup.main.h2)
    last_video_title = soup.main.h2.find_all('a')[0].text
    last_video_name = last_video_title.split("[")[0]
    last_video_num = last_video_title.split("[")[1].split("]")[0]
    unread = "v" if comic["my_process"] != last_video_num else ""

    data = [
        unread,
        comic["my_process"],
        last_video_num,
        comic["url"],
        last_video_name
    ]
    print(data)
    set_comic_list.append(data)


set_comic_list_to_csv(filename, set_comic_list)
