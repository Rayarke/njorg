import configparser
import os
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import pymysql
import wget
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
host = 'http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjj/'


def dbConnect(article_link, article_title, article_content, article_author, article_annex_link, article_time):
    config = configparser.ConfigParser()
    config.read('/Users/schrodinger/PycharmProjects/aa/conf/connect', encoding='utf-8')
    ip = config.get('mysql-db', 'ip')
    db_name = config.get('mysql-db', 'db_name')
    username = config.get('mysql-db', 'username')
    password = config.get('mysql-db', 'password')
    print(ip, db_name, username, password)
    conn = pymysql.connect(ip, username, password, db_name, charset='utf8')
    cur = conn.cursor()
    sql = "insert into njorg(article_link,article_title,article_content,article_author,article_annex_link,article_time,created_time) values(%s,%s,%s,%s,%s,%s,%s)"
    article_link = article_link
    article_title = article_title
    article_content = article_content
    article_author = article_author
    article_annex_link = article_annex_link
    article_time = article_time
    created_time = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "%Y-%m-%d %H:%M:%S")
    par = (
        article_link, article_title, article_content, article_author, article_annex_link, article_time, created_time)
    conn.ping(reconnect=True)
    cur.execute(sql, par)
    conn.commit()
    conn.close()


def getHref():
    res = urllib.request.urlopen('http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjj/').read().decode('utf-8')
    home_page = BeautifulSoup(res, 'html.parser')
    # 通过 attrs 查看 class 名称为 dpgl_con的标签
    li = home_page.find(attrs={'class': 'dpgl_con'})
    # 对于还是tag的元素标签可以再次使用 find()||find_all():target 标签名称查找
    paths = li.find_all(target="_blank")
    for one in paths:
        href_orign = one['href']
        # python分割字符串 str[2:] 其实变相当作数组进行处理
        href_ex = href_orign[2:]
        url = host + href_ex
        print(url)
        article(url)


def article(url):
    article_link = url
    article_title = ''
    article_content = ''
    article_author = ''
    article_annex_link = ''
    article_time = ''
    if url[-5:] == '.html':
        res = urllib.request.urlopen(url).read().decode('utf-8')
        page = BeautifulSoup(res, 'html.parser')
        # print(page)
        tyxl_title = page.find(attrs={'class': 'tyxl_title'})
        article_title = tyxl_title.h1.get_text()
        article_time = tyxl_title.p.get_text()[:24]
        article_author = tyxl_title.p.get_text()[27:35]
        tyxl_ncon = page.find(attrs={'class': 'tyxl_ncon'})
        new_tag = page.new_tag("div", id="lambs")
        new_tag.append(tyxl_ncon)
        tyxl_ncon_p = new_tag.find_all('p')
        # print(tyxl_ncon_p)
        words = []
        for word in tyxl_ncon_p:
            words.append(word.prettify())
        article_content = ''.join(words)
        print(article_content)
    elif url[-4:] == '.pdf':
        folder = '/Users/schrodinger/njorg/download_annex'
        dirt = Path(folder)
        if dirt.exists():
            wget.download(url, '/Users/schrodinger/njorg/download_annex')
        else:
            os.makedirs(folder)
            wget.download(url, '/Users/schrodinger/njorg/download_annex')
    else:
        pass
    dbConnect(article_link, article_title, article_content, article_author, article_annex_link, article_time)


if __name__ == '__main__':
    getHref()
