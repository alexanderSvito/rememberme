import requests
import json
import time
from bs4 import BeautifulSoup as BS


url = "https://progress.lawlessfrench.com{}"

links = ['/learn/theme/128', '/learn/theme/239', '/learn/theme/255', '/learn/theme/336', '/learn/theme/337', '/learn/theme/342', '/learn/theme/431', '/learn/theme/452', '/learn/theme/1', '/learn/theme/6', '/learn/theme/10', '/learn/theme/18', '/learn/theme/23', '/learn/theme/26', '/learn/theme/27', '/learn/theme/33', '/learn/theme/34', '/learn/theme/264', '/learn/theme/277', '/learn/theme/281', '/learn/theme/290', '/learn/theme/293', '/learn/theme/298', '/learn/theme/320', '/learn/theme/349', '/learn/theme/369', '/learn/theme/382', '/learn/theme/387', '/learn/theme/430', '/learn/theme/432', '/learn/theme/442', '/learn/theme/450', '/learn/theme/493', '/learn/theme/939774', '/learn/theme/961275', '/learn/theme/1015270', '/learn/theme/1133510', '/learn/theme/1188564', '/learn/theme/1253443', '/learn/theme/1294914', '/learn/theme/1337641', '/learn/theme/1369608', '/learn/theme/1399776', '/learn/theme/1603259', '/learn/theme/1621039', '/learn/theme/2325226', '/learn/theme/2619872', '/learn/theme/2697544', '/learn/theme/2782671', '/learn/theme/3907231', '/learn/theme/4667287', '/learn/theme/5639296', '/learn/theme/6424119', '/learn/theme/6561558', '/learn/theme/6608127', '/learn/theme/6608211', '/learn/theme/6608263', '/learn/theme/7388290', '/learn/theme/8371585', '/learn/theme/9864293', '/learn/theme/10290712', '/learn/theme/7', '/learn/theme/238', '/learn/theme/258', '/learn/theme/259', '/learn/theme/279', '/learn/theme/282', '/learn/theme/283', '/learn/theme/287', '/learn/theme/295', '/learn/theme/297', '/learn/theme/300', '/learn/theme/303', '/learn/theme/308', '/learn/theme/309', '/learn/theme/311', '/learn/theme/366', '/learn/theme/390', '/learn/theme/444', '/learn/theme/445', '/learn/theme/446', '/learn/theme/448', '/learn/theme/449', '/learn/theme/492', '/learn/theme/895820', '/learn/theme/919118', '/learn/theme/922879', '/learn/theme/925242', '/learn/theme/939623', '/learn/theme/939715', '/learn/theme/939762', '/learn/theme/954584', '/learn/theme/992202', '/learn/theme/1013209', '/learn/theme/1048233', '/learn/theme/1061740', '/learn/theme/1127826', '/learn/theme/1149614', '/learn/theme/1179046', '/learn/theme/1200603', '/learn/theme/1201689', '/learn/theme/1270603', '/learn/theme/1280680', '/learn/theme/1365448', '/learn/theme/1442883', '/learn/theme/1442915', '/learn/theme/1469356', '/learn/theme/1512981', '/learn/theme/1543661', '/learn/theme/1583610', '/learn/theme/1666922', '/learn/theme/1693295', '/learn/theme/1693667', '/learn/theme/1714087', '/learn/theme/1903765', '/learn/theme/2010949', '/learn/theme/2031431', '/learn/theme/2167325', '/learn/theme/2265649', '/learn/theme/2663149', '/learn/theme/3409284', '/learn/theme/3449405', '/learn/theme/3744352', '/learn/theme/3907306', '/learn/theme/3907372', '/learn/theme/4071857', '/learn/theme/7838200', '/learn/theme/8050112', '/learn/theme/9611820', '/learn/theme/10511726', '/learn/theme/10528085', '/learn/theme/11059328', '/learn/theme/11469989', '/learn/theme/11625784', '/learn/theme/5', '/learn/theme/251', '/learn/theme/253', '/learn/theme/256', '/learn/theme/257', '/learn/theme/260', '/learn/theme/261', '/learn/theme/265', '/learn/theme/280', '/learn/theme/301', '/learn/theme/306', '/learn/theme/307', '/learn/theme/426', '/learn/theme/890504', '/learn/theme/945659', '/learn/theme/954342', '/learn/theme/991741', '/learn/theme/1042983', '/learn/theme/1118481', '/learn/theme/1156091', '/learn/theme/1163204', '/learn/theme/1288057', '/learn/theme/1320528', '/learn/theme/1323032', '/learn/theme/1381228', '/learn/theme/1453148', '/learn/theme/1456942', '/learn/theme/1488365', '/learn/theme/1513111', '/learn/theme/1543399', '/learn/theme/1564577', '/learn/theme/1583319', '/learn/theme/1583615', '/learn/theme/1642660', '/learn/theme/1659846', '/learn/theme/1685090', '/learn/theme/1760884', '/learn/theme/1776305', '/learn/theme/1806848', '/learn/theme/2119749', '/learn/theme/2222059', '/learn/theme/2722014', '/learn/theme/3812349', '/learn/theme/3907147', '/learn/theme/3907458', '/learn/theme/3975140', '/learn/theme/3975230', '/learn/theme/4475905', '/learn/theme/4493637', '/learn/theme/4644804', '/learn/theme/5345708', '/learn/theme/6620746', '/learn/theme/7123797', '/learn/theme/8992053', '/learn/theme/9059506', '/learn/theme/10342629', '/learn/theme/10344675', '/learn/theme/10344706', '/learn/theme/10346017', '/learn/theme/10789639', '/learn/theme/11485141', '/learn/theme/11733612', '/learn/theme/11749073', '/learn/theme/21', '/learn/theme/252', '/learn/theme/877355', '/learn/theme/946769', '/learn/theme/1073924', '/learn/theme/1125897', '/learn/theme/1241979', '/learn/theme/1738752', '/learn/theme/3603304', '/learn/theme/3941525', '/learn/theme/4050945', '/learn/theme/4908298', '/learn/theme/6501824', '/learn/theme/6886232', '/learn/theme/7018048', '/learn/theme/7129403', '/learn/theme/7603528', '/learn/theme/8336071', '/learn/theme/8826063', '/learn/theme/8946524', '/learn/theme/9104731', '/learn/theme/9430285', '/learn/theme/4386711', '/learn/theme/7854506', '/learn/theme/8299030', '/learn/theme/10501607']


vocab = {}

def parse_page(link):
    data = BS(requests.get(url.format(link)).content)

    if data.find("table", attrs={"class": "table-vocab-list"}):
        for row in data.find("table", attrs={"class": "table-vocab-list"}).find_all("tr"):
            if len(row.find_all("td")) == 3:
                fr, pl, en = row.find_all("td")
                vocab[en.text] = fr.text

    with open("en-fr.json", "w") as f:
        json.dump(vocab, f, indent=2, ensure_ascii=False)

for i in links:
    print("parsing: {}".
          format(url.format(i)))
    parse_page(i)
    print('done')
    time.sleep(1)
