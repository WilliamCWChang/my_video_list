import csv
import requests
from bs4 import BeautifulSoup
import re


def get_comic_list_from_markdown(filename):
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


def get_video_info(url):
    video_info = {
        "title": None,
        "now": -1,
    }
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if len(soup.find_all("h2")) != 0:
        titles = soup.find_all('h2')
        print(titles[0].text)
        if titles[0].text == '近期文章':
            return video_info

        now_num_list = []
        video_info["title"] = titles[0].text.split("[")[0]
        for title in titles:
            title = title.text
            if "[" in title:
                now_num = title.split("[")[1].split("]")[0]
                now_num = ''.join(re.findall('[0-9]+', now_num))
                now_num = -1 if now_num == '' else now_num
                now_num_list.append(int(now_num))
        video_info["now"] = max(now_num_list)
    return video_info


def main():
    input_filename = 'Readme.md'
    output_filename = 'Readme2.md'
    set_comic_list = []
    # print(input_filename)

    # print(get_comic_list_from_markdown(input_filename))

    for comic in get_comic_list_from_markdown(input_filename):
        print(comic)
        unread = comic["unread"]

        if comic["enable"]:
            video_info = get_video_info(comic["url"])
            print(video_info["title"], video_info["now"])

            if video_info["now"] is -1:
                continue

            unread = True if int(comic["my_process"]) != int(video_info["now"]) else False
        data = [
            "v" if comic["enable"] else " ",
            "v" if unread else " ",
            str(comic["my_process"]).zfill(2),
            str(video_info["now"]).zfill(2).strip(" "),
            comic["url"].replace(" ", ""),
            video_info["title"].strip()
        ]
        set_comic_list.append(data)

    set_comic_list = sort_comic_list(set_comic_list)

    data = ["Enable|Unread|My|Now|Url|Name"]
    set_comic_list.insert(0, data)
    data = [":-:|:-:|:-:|:-:|:-:|:-:"]
    set_comic_list.insert(1, data)
    set_comic_list_to_markdown(output_filename, set_comic_list)


if __name__ == '__main__':
    # main()
    print("A")
