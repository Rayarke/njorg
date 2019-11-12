import configparser
import time
import urllib.request
from datetime import datetime

import pymysql
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
host = 'http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjj/'

def dbConnect():
    config = configparser.ConfigParser()
    config.read('/Users/schrodinger/njorg/config/mysql', encoding='utf-8')
    ip = config.get('mysql-db', 'ip')
    db_name = config.get('mysql-db', 'db_name')
    username = config.get('mysql-db', 'username')
    password = config.get('mysql-db', 'password')
    print(ip, db_name, username, password)
    conn = pymysql.connect('ip', 'root', 'password', 'dbname')
    cur = conn.cursor()
    sql = "insert into njorg(article_link,article_title,article_content,article_author,article_annex_link,article_time,created_time) values(%s,%s,%s,%s,%s,%s,%s)"
    article_link = 'article_link'
    article_title = 'article_title'
    article_content = 'article_content'
    article_author = 'article_author'
    article_annex_link = 'article_annex_link'
    article_page_time = '2019-11-12'
    article_time = datetime.strptime(article_page_time, '%Y-%m-%d')
    created_time =datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"%Y-%m-%d %H:%M:%S")
    # created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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
    if url[-4:] == '.pdf':
        response = urllib.request.urlopen(url)
        file = open("document.pdf", 'w')
        file.write(response.read())
        file.close()
    elif url[-4:] == '.html':
        res = urllib.request.urlopen(url).read().decode('utf-8')
        page = BeautifulSoup(res, 'html.parser')
    else:
        pass

if __name__ == '__main__':
    getHref()
