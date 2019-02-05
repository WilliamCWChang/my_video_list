import requests
from bs4 import BeautifulSoup
# from urllib.parse import unquote
import re


url = "https://anime1.me/2018年秋季新番"
# url = unquote(url)
# print(url)

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
pattern = re.compile("\/\?cat=*")


print("comic = {")
for link in soup.find_all('a'):
    # print(unquote(link.get('href')))
    if pattern.match(link.get('href')):
        print('"' + link.text + '":"' + "https://anime1.me" + link.get('href') + '",')
print("}")
