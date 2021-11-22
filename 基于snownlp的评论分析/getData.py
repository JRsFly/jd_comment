import requests
from bs4 import BeautifulSoup
import bs4
import urllib.parse
from pandas.core.frame import DataFrame
import json
import pandas as pd
from snownlp import SnowNLP
from snownlp import sentiment
from fake_useragent import UserAgent
#将报错信息省略
requests.packages.urllib3.disable_warnings()
num = 0
#这里采用的是使用快代理的隧道ip实现ip切换
tunnel = "tps***.kdlapi.com:15818"
username = "username
password = "password"
#对于ip进行切换，防止同一ip多次爬取后，ip被封
def get_proxies():
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    return proxies

def train():
    print("开始训练数据集...")
    sentiment.train('negative.txt', 'positive.txt')#自己准备数据集
    sentiment.save('sentiment.marshal')#保存训练模型
    #python2保存的是sentiment.marshal；python3保存的是sentiment.marshal.3
    "训练完成后，将训练完的模型，替换sentiment中的模型"

#使用request库获取html基本信息
def getHTMLText(url,Proxies):
    #time.sleep(5)
    ua = UserAgent()
    Headers = {
    'Connection':'close',
    'User-Agent':ua.random
}
    while True:
        try:
            sess = requests.Session()
            sess.keep_alive = False  # 关闭多余连接
            r = sess.get(url,headers = Headers,proxies=Proxies,verify=False)
            r.encoding = r.apparent_encoding
            rtext =r.text
            r.close()
            return rtext
        except:

            print("try to connectttt...")

#获得网页文本信息，为了防止ip被封导致返回为空，使用循环语句直至获取数据非空时返回
def get_text(url):
    Proxies = get_proxies()
    text = getHTMLText(url,Proxies)
    while text == "":
        Proxies = get_proxies()
        print("try to connect....")
        text = getHTMLText(url,Proxies)
    return text

#通过html文本信息，进行分析，最终得出商品的价格，名称，编号 
def fillUnivList(price_set,name_set,product_ID_set,html):
    soup = BeautifulSoup(html, "html.parser")
    prices = soup.find_all('div',class_ = 'p-price')
    names = soup.find_all('div',class_ = 'p-name p-name-type-2')
    product_IDs = soup.find_all('li',class_ = 'gl-item')
    for price in prices:
        price = price.text.split()
        price_set.append(price[0])
    for name in names:
        name = name.find_all('em')[0]
        name = name.text
        name_set.append(name)
    for product_ID in product_IDs:
        product_ID_set.append(product_ID['data-sku'])
    return ""

#获得商品的具体参数，并输出
def  intro_product(product_id):
    url = "https://item.jd.com/"+str(product_id)+".html"
    html = get_text(url)
    soup = BeautifulSoup(html,"html.parser")
    li = soup.find_all('ul',class_ = 'parameter2 p-parameter-list')
    for tr in li:
        tr = tr.text.strip('\n')
        return tr
    #print(tr)
    '''for i in range(len(tr)):
        if i % 2 == 0:
            intro_product_id_set.append(tr[i])
        else:
            intro_product_key_set.append(tr[i])'''

