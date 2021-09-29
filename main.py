import requests
import bs4
import re
import os
import sqlite3


URL = 'https://www.ptt.cc/bbs/Beauty/index3791.html'

# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}
response = requests.get(URL, headers=my_headers)

soup = bs4.BeautifulSoup(response.text, "html.parser")
articles = soup.find_all('a')

for ar in articles:
    if ar.text[0:4] != '[正妹]':
        continue

    # 文章標題
    print("標題：" + ar.text)
    # 文章網址
    print("網址：https://www.ptt.cc" + ar.get('href'))

    URL = "https://www.ptt.cc" + ar.get('href')

    response = requests.get(URL, headers=my_headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    header = soup.find_all('span', 'article-meta-value')

    # 作者
    author = header[0].text
    # 看版
    board = header[1].text
    # 標題
    title = header[2].text
    # 日期
    date = header[3].text

    # 查找所有html 元素 抓出內容
    main_container = soup.find(id='main-container')
    # 把所有文字都抓出來
    all_text = main_container.text
    # 把整個內容切割透過 "-- " 切割成2個陣列
    pre_text = all_text.split('--')[0]

    # 把每段文字 根據 '\n' 切開
    texts = pre_text.split('\n')

    contents = texts[2:]

    img_list = []
    for img_url in contents:
        # 只抓圖檔連結
        result = re.findall(
            'https?://\S+?/\S+?\.(?:jpg|jpeg|gif|png)', img_url)
        if len(result) == 0:
            continue

        img_list.append(result[0])

    # 內容
    content = '\n'.join(img_list)

    # 顯示
    print('作者：' + author)
    print('看板：' + board)
    print('標題：' + title)
    print('日期：' + date)
    print('內容：' + content)

    # 過濾特殊字元
    path = title[0:4] + ''.join(filter(str.isalnum, title[5:]))

    # 建立資料夾存照片
    if not os.path.isdir(path):
        os.mkdir(path)

    for img_url in img_list:
        arr_name = img_url.split('/')
        response = requests.get(img_url)
        f = open(path + '/' + arr_name[-1], 'wb')
        f.write(response.content)
        f.close()
