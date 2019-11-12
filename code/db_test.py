import configparser
import time
from datetime import datetime
import pymysql


def dbConnect():
    config = configparser.ConfigParser()
    config.read('/Users/schrodinger/njorg/config/mysql', encoding='utf-8')
    ip = config.get('mysql-db', 'ip')
    db_name = config.get('mysql-db', 'db_name')
    username = config.get('mysql-db', 'username')
    password = config.get('mysql-db', 'password')
    conn = pymysql.connect('ip', 'root', 'password', 'dbname')
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


if __name__ == '__main__':
    dbConnect()
