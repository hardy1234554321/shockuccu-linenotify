# 載入需要的模組
import requests
import bs4
import re
import os
import time
import datetime
import sqlite3


def lineNotifyMessage(token, message, img, isNotificationDisabled = False):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        'message': message,
        'imageThumbnail': img,
        'imageFullsize': img,
        'notificationDisabled': isNotificationDisabled
    }

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    print(r.status_code)
    time.sleep(1)
    # cmd = 'curl -D - -H "Authorization: Bearer %s" https://notify-api.line.me/api/status' % token
    # os.system(cmd)


def spider_ptt_beauty(token):
    my_headers = {
        'cookie': 'over18=1;'
    }
    list_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    response = requests.get(list_url, headers=my_headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all('a')
    for ar in articles:
        # 篩選文章條件
        if ar.text[0:4] != '[正妹]':
            continue
        if '肉特' in ar.text:
            continue


        article_url = 'https://www.ptt.cc%s' % ar.get('href')

        # 檢查是否發送過
        sql = "SELECT * FROM articles WHERE a_url = '%s'" % article_url
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            print('暫無新文章 %s' % datetime.datetime.now())
            time.sleep(1)
            continue


        response = requests.get(article_url, headers=my_headers)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # 表頭資訊
        header = soup.find_all('span', 'article-meta-value')
        # 作者
        author = header[0].text
        # 看版
        board = header[1].text
        # 標題
        title = header[2].text
        # 日期
        date = header[3].text

        main_container = soup.find(id='main-container')
        all_text = main_container.text
        pre_text = all_text.split('--')[0]

        # 把每段文字 根據 '\n' 切開
        texts = pre_text.split('\n')
        contents = texts[2:]

        # 只抓jpg gif png
        img_list = []
        for img_url in contents:
            # 只抓圖檔連結
            result = re.findall(
                'https?://\S+?/\S+?\.(?:jpg|gif|png)', img_url)
            if len(result) == 0:
                continue
            img_list.append(result[0])

        # 內容轉文字
        content = '\n'.join(img_list)

        # 顯示
        msg = '\n'
        msg += '\n作者：%s' % author
        msg += '\n看板：%s' % board
        msg += '\n標題：%s' % title
        msg += '\n日期：%s' % date
        msg += '\n網址：%s' % article_url
        print(msg)

        # Lint Notify 文章資訊
        lineNotifyMessage(token=token, message=msg, img='')

        # 紀錄文章資訊
        sql = "INSERT INTO 'articles' ('id','a_url','a_author','a_title','a_type') VALUES (NULL,'%s','%s','%s','%s')" % (
            article_url, author, title, 'PTT')
        c.execute(sql)
        conn.commit()

        # Lint Notify 圖片
        for img_url in img_list:
            img_msg = '\n%s' % (img_url)
            print(img_msg)
            lineNotifyMessage(token=token, message=img_msg, img=img_url, isNotificationDisabled=True)
            time.sleep(1)



def spider_dcard_sex(token):
    my_headers = {
        'cookie': 'over18=1;'
    }
    list_url = 'https://www.dcard.tw/f/sex?latest=true'
    response = requests.get(list_url, headers=my_headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all('a')
    for ar in articles:
        article_url = 'https://www.dcard.tw%s' % ar.get('href')
        if '/f/sex/p/' not in article_url:
            continue

        # 檢查是否發送過
        sql = "SELECT * FROM articles WHERE a_url = '%s'" % article_url
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            print('暫無新文章 %s' % datetime.datetime.now())
            time.sleep(1)
            continue

        # 載入文章
        response = requests.get(article_url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # 檢查文章有沒有不見
        content = soup.find('h1', 'sc-7mzcsk-2')
        if content:
            if content.string == 'Oh！文章不見了':
                continue

        # 標題
        h1_title = soup.find('h1', 'sc-1932jlp-0')
        title = h1_title.text

        img_list = []
        for img_url in soup.find_all('img'):
             # 只抓圖檔連結
            result = re.findall(
                'https?://imgur.dcard.tw?\S+?/\S+?\.(?:jpg|gif|png)', img_url.get('src'))
            if len(result) == 0:
                continue
            img_list.append(result[0])

        # 內容轉文字
        content = '\n'.join(img_list)

        # 顯示
        msg = '\n'
        msg += '\n標題：%s' % title
        msg += '\n網址：%s' % article_url
        print(msg)
        lineNotifyMessage(token=token, message=msg, img='')

        # 紀錄文章資訊
        sql = "INSERT INTO 'articles' ('id','a_url','a_author','a_title','a_type') VALUES (NULL,'%s','%s','%s','%s')" % (
            article_url, 'dcard', title, 'DCARD')
        c.execute(sql)
        conn.commit()

        for img_url in img_list:
            img_msg = '\n%s' % (img_url)
            print(img_msg)
            lineNotifyMessage(token=token, message=img_msg, img=img_url, isNotificationDisabled=True)
            time.sleep(1)



if __name__ == "__main__":
    while (1):
        # create DATABASE
        conn = sqlite3.connect('db/shockuccuptt.db')
        c = conn.cursor()

        # create TABLE
        sql = "CREATE TABLE IF NOT EXISTS 'articles' (\
                'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                'a_url' TEXT NOT NULL,\
                'a_author' TEXT NOT NULL,\
                'a_title' TEXT NOT NULL,\
                'a_type' TEXT NOT NULL\
            )"
        c.execute(sql)
        conn.commit()

        # Ptt表特版
        token = '<access_token>'
        spider_ptt_beauty(token)
        # Dcard西斯版
        token = 'access_token'
        spider_dcard_sex(token)

        conn.close()



