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
        file.write("|Enable|Unread|My|Now|Url|Name |\n")
        file.write("|:-:|:-:|:-:|:-:|:-:|:-:|\n")
        for comic in comic_list:
            # file.write(comic)
            file.write("|  " + " | ".join(comic) + "|\n")


def sort_comic_list(comic_list):
    enable_read_list = []
    enable_unread_list = []
    disable_list = []

    for index, comic in enumerate(comic_list):
        # print(comic)
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
        # print(titles)
        if titles[0].text == '近期文章':
            return video_info

        now_num_list = []
        video_info["title"] = titles[0].text.split("[")[0]
        for title in titles:
            title = title.text
            if "[" in title:
                now_num = title.split("[")[1].split("]")[0]
                now_num = ''.join(re.findall('[0-9]+.', now_num))
                now_num = -1 if now_num == '' else now_num
                now_num_list.append(float(now_num))
        video_info["now"] = int(max(now_num_list))
    return video_info


def refresh_data(filename):
    set_comic_list = []
    for comic in get_comic_list_from_markdown(filename):
        print((comic["title"]))        
        if comic["enable"]:
            try:
                video_info = get_video_info(comic["url"])
                comic["now"] = video_info["now"]
                comic["title"] = video_info["title"]
            except Exception as e:
                # Just Pass, And Do nothing!
                pass
            # Can not find anything in this url.
            if video_info["now"] is -1:
                continue

        data = [
            "v" if comic["enable"] else " ",
            "v" if int(comic["my_process"]) != int(comic["now"]) else " ",
            str(comic["my_process"]).strip().zfill(2),
            str(comic["now"]).strip().zfill(2),
            comic["url"].strip().replace(" ", ""),
            comic["title"].strip()
        ]
        set_comic_list.append(data)
    return set_comic_list


def main():
    input_filename = 'Readme.md'
    output_filename = 'Readme.md'
    set_comic_list = refresh_data(input_filename)
    set_comic_list = sort_comic_list(set_comic_list)
    set_comic_list_to_markdown(output_filename, set_comic_list)

if __name__ == '__main__':
    main()
