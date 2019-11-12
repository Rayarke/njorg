import urllib.request

from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
host = 'http://njna.ngorg.gov.cn/cxrc/cxrczc/zcjj/'


def getHomePage():
        res = urllib.request.urlopen('http://njna.ngorg.gov.cn/cxrc/cxrczc/zcjj').read().decode('utf-8')
        home_page = BeautifulSoup(res, 'html.parser')
        # 通过attrs class 名称
        li = home_page.find(attrs={'class':'dpgl_con'})
        paths = li.find_all(target="_blank")
        # print(paths)
        for one in paths:
            href_orign = one['href']
            href_ex = href_orign[2:]
            address = host+href_ex
            # print(address)
            wenzhang(address)


def wenzhang(address):
    res = urllib.request.urlopen(address).read().decode('utf-8')
    home_page = BeautifulSoup(res, 'html.parser')
    h1 = home_page.find('h1')

    for i in h1:
        # print(i)
        div = home_page.find(attrs={'id': 'con'})
        for j in div:
            for k in j:
                # print(k)
                for l in k:
                    print(l)
if __name__ == '__main__':
    getHomePage()