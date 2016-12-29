from multiprocessing.dummy import Pool as ThreadPool
import threading
import requests
from lxml import html as html_parser

def getpage():
    i = 0
    while 1 :
        new = 'https://book.douban.com/tag/%E9%9D%92%E6%98%A5?start={}&type=T'.format(i*20)
        data = requests.get(new)
        selector = html_parser.fromstring(data.text)
        book_itemlist = selector.xpath('//div[@id="subject_list"]/p[@class="pl2"]/text()')
        if book_itemlist:
            break
        else :
            i +=1
    print(i)
    return i

def url(num,urls_list):
    for i in range(0,num):
        new = 'https://book.douban.com/tag/%E9%9D%92%E6%98%A5?start={}&type=T'.format(i * 20)
        urls_list.append(new)
    return urls_list

def getsource(url):
    data = requests.get(url)
    selector = html_parser.fromstring(data.text)
    bookItemList = selector.xpath('//div[@class="info"]')
    bookList = []

    for eachBook in bookItemList:
        bookDict = {}
        title = eachBook.xpath('h2[@class=""]/a/@title')
        # print(title)
        star = eachBook.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
        price = eachBook.xpath('div[@class="pub"]/text()')
        price = str(price[0]) if price else ''
        talked = eachBook.xpath('div[@class="star clearfix"]/span[@class="pl"]/text()')
        talked = str(talked[0]) if talked else ''
        bookList.append({
            'title': title[0] if title else '',
            'star': star[0] if star else '',
            'price': price.replace(" ",'').replace('\n',''),
            'talked': talked.replace(" ", '').replace('\n', '')
        })
    return bookList

if __name__ == '__main__' :
    num = getpage()
    urls=[]
    url = url(num,urls)
    print(url)
    pool = ThreadPool(20)
    results = pool.map(getsource, url)
    print(results)
    pool.close()
    pool.join()