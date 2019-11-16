
import configparser
import os
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import pymysql
import wget
from bs4 import BeautifulSoup

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
        sty = page.find('style')
        sty.decompose()
        print(page)
        # print(page)
        tyxl_title = page.find(attrs={'class': 'tyxl_title'})
        article_title = tyxl_title.h1.get_text()
        article_time = tyxl_title.p.get_text()[:24]
        article_author = tyxl_title.p.get_text()[27:35]
        tyxl_ncon = page.find(attrs={'class': 'tyxl_ncon'})
        s = tyxl_ncon.select('style')[1]
        # print(s)
        # print(type(s))
        s.decompose()
        # print(tyxl_ncon)
    #     new_tag = page.new_tag("div", id="lambs")
    #     new_tag.append(tyxl_ncon)
    #     tyxl_ncon_p = new_tag.find_all('p')
    #     # print(tyxl_ncon_p)
    #     words = []
    #     for word in tyxl_ncon_p:
    #         words.append(word.prettify())
    #     article_content = ''.join(words)
    #     print(article_content)
    # elif url[-4:] == '.pdf':
    #     folder = '/Users/schrodinger/njorg/download_annex'
    #     dirt = Path(folder)
    #     if dirt.exists():
    #         wget.download(url, '/Users/schrodinger/njorg/download_annex')
    #     else:
    #         os.makedirs(folder)
    #         wget.download(url, '/Users/schrodinger/njorg/download_annex')
    # else:
    #     pass
    # print(article_link, article_title, article_content, article_author, article_annex_link, article_time)

if __name__ == '__main__':
    # article('http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjj/201711/t20171108_491221.html')
    print(len('http://njna.nanjing.gov.cn/cxrc/cxrczc/zcjd/201903/'))