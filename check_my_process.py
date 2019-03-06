import csv
import requests
from bs4 import BeautifulSoup


def get_comic_list_from_csv(csvfilename):
    comic_list = []
    with open(filename, encoding='utf8') as file:
        for index, row in enumerate(file.readlines()):
            if index < 2:
                continue
            if len(row) < 3:
                continue
            row = row.split("|")
            # print(row)
            comic_list.append(
                {
                    "my_process": int(row[2]),
                    "url": row[4],
                })
    return comic_list



def set_comic_list_to_csv(filename, comic_list):
    with open(filename, newline='', encoding='utf8', mode='w') as file:
        # data_list = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for comic in comic_list:
            # file.write(comic)
            file.write(" | "+" | ".join(comic)+" |\n")


filename = 'Readme.md'

set_comic_list = []
data = ["Read|My|Now|Url|Name"]
set_comic_list.append(data)
data = [":-:|:-:|:-:|:-:|:-:"]
set_comic_list.append(data)

for index, comic in enumerate(get_comic_list_from_csv(filename)):
    print(index, comic)

    r = requests.get(comic["url"])
    soup = BeautifulSoup(r.text, 'html.parser')

    if "近期文章" in soup.main.h2.text:
        print("The page is not found. url={}".format(comic["url"]))
        continue

    # print(soup.main.h2)
    last_video_title = soup.main.h2.find_all('a')[0].text
    last_video_name = last_video_title.split("[")[0]
    last_video_num = last_video_title.split("[")[1].split("]")[0]
    unread = "v" if int(comic["my_process"]) != int(last_video_num) else ""

    data = [
        unread,
        str(comic["my_process"]),
        last_video_num,
        comic["url"],
        last_video_name
    ]
    # print(data)
    set_comic_list.append(data)


set_comic_list_to_csv(filename, set_comic_list)
