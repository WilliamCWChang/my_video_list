import csv
import requests
from bs4 import BeautifulSoup


def get_comic_list_from_markdown(csvfilename):
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
                    "enable": True if "v" in row[1].lower() else False,
                    "unread": True if "v" in row[2].lower() else False,
                    "my_process": int(row[3]),
                    "now": row[4],
                    "url": row[5],
                    "title": row[6],
                })
    return comic_list


def set_comic_list_to_markdown(filename, comic_list):
    with open(filename, newline='', encoding='utf8', mode='w') as file:
        # data_list = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for comic in comic_list:
            # file.write(comic)
            file.write(" | " + " | ".join(comic) + " |\n")


def sort_comic_list(comic_list):
    enable_read_list = []
    enable_unread_list = []
    disable_list = []

    for index, comic in enumerate(comic_list):
        print(comic)
        enable = comic[0]
        unread = comic[1]

        if enable == "v":
            if unread == "v":
                enable_unread_list.append(comic)
            else:
                enable_read_list.append(comic)
        else:
            disable_list.append(comic)

    return enable_unread_list + enable_read_list + disable_list


filename = 'Readme.md'

set_comic_list = []


for comic in get_comic_list_from_markdown(filename):
    print(comic)
    unread = comic["unread"]

    last_video_num = comic["now"]
    last_video_name = comic["title"]
    if comic["enable"]:
        r = requests.get(comic["url"])
        soup = BeautifulSoup(r.text, 'html.parser')

        if "近期文章" in soup.main.h2.text:
            # print("The page is not found. url={}".format(comic["url"]))
            continue

        # print(soup.main.h2)

        video_title = soup.main.find_all('h2')[0].text.split("[")[0]

        last_video_num = -1
        for text in soup.main.find_all('h2'):
            if video_title not in text.text:
                if "文章分頁" in text.text:
                    continue
                elif "文章導覽" in text.text:
                    continue

                else:
                    print("video_title = {}\t text.text = {}".format(video_title, text.text))
                    last_video_num = -1
                    break

            video_num = text.text.split("[")[1].split("]")[0]
            if video_num.isdigit():
                if int(video_num) > int(last_video_num):
                    last_video_num = int(video_num)

        if last_video_num is -1:
            # print(comic["url"].replace(" ", ""))
            continue

        last_video_title = soup.main.h2.find_all('a')[0].text
        last_video_name = last_video_title.split("[")[0]
        unread = True if int(comic["my_process"]) != int(last_video_num) else False
    data = [
        "v" if comic["enable"] else " ",
        "v" if unread else " ",
        str(comic["my_process"]).zfill(2),
        str(last_video_num).zfill(2).strip(" "),
        comic["url"].replace(" ", ""),
        last_video_name.strip()
    ]
    set_comic_list.append(data)


print(set_comic_list)

set_comic_list = sort_comic_list(set_comic_list)


data = ["Enable|Unread|My|Now|Url|Name"]
set_comic_list.insert(0, data)
data = [":-:|:-:|:-:|:-:|:-:|:-:"]
set_comic_list.insert(1, data)
set_comic_list_to_markdown(filename, set_comic_list)
