import configparser
import time
import pymysql
import wget
from pathlib import Path
import os
def dbConnect():
    config = configparser.ConfigParser()
    config.read('/Users/schrodinger/njorg/config/mysql', encoding='utf-8')
    ip = config.get('mysql-db', 'ip')
    db_name = config.get('mysql-db', 'db_name')
    username = config.get('mysql-db', 'username')
    password = config.get('mysql-db', 'password')
    conn = pymysql.connect(ip, username, password, db_name)
    cur = conn.cursor()
    sql = "insert into njorg(article_link,article_title,article_content,article_author,article_annex_link,article_time,created_time) values(%s,%s,%s,%s,%s,%s,%s)"
    article_link = 'article_link'
    article_title = 'article_title'
    article_content = 'article_content'
    article_author = 'article_author'
    article_annex_link = 'article_annex_link'
    article_time = '2019-11-12'
    created_time =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    par = (
    article_link, article_title, article_content, article_author, article_annex_link, article_time, created_time)
    conn.ping(reconnect=True)
    cur.execute(sql, par)
    conn.commit()
    conn.close()

def pdfDownload(url):
    folder = '/Users/schrodinger/njorg/download_annex'
    dirt = Path(folder)
    if dirt.exists():
        wget.download(url, '/Users/schrodinger/njorg/download_annex')
    else:
        os.makedirs(folder)
        wget.download(url, '/Users/schrodinger/njorg/download_annex')
if __name__ == '__main__':
    pdfDownload('http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjj/201806/P020181021126493226218.pdf')
