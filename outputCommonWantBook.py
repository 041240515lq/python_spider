#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 设置编码格式为utf-8，为了可以打印出中文字符
import sys
# 导入urllib2模块，用于通过url获取网页的内容
import urllib.request
# 导入BeautifulSoup模块(需要安装)，用于解析网页的内容
from bs4 import BeautifulSoup
# 导入python操作excel模块
import xlwt
import importlib
importlib.reload(sys)

# 通过xlwt(python操作office的模块)设置utf编码格式，并返回一个excel对象'book'
book = xlwt.Workbook(encoding='utf-8', style_compression=0)

# 通过这个book对象新建一个sheet，命名为我的豆瓣想读的书
sheet = book.add_sheet('按收藏时间排序', cell_overwrite_ok=True)

# 定义一个全局的行数n，为了下面parser_to_excel方法写入excel时可以找到从哪一行开始写入
n = 0
urlSet_list = list()
infoDict_list = list()

urlSetTemp = (set(), set())  # 存储每位读者的想读的书的链接
infoDictTemp = (dict(), dict())  # 存储图书的具体信息
# urlSet = set()
# infoDict = dict()
num = 0

count = 0

# list_referer = ['https://book.douban.com/people/154001100/collect?sort=rating&start=0&mode=grid&tags_sort=count',
#                     'https://book.douban.com/people/138083612/collect?sort=time&start=0&mode=grid&tags_sort=count']
# 通过url得到页面全部内容
def get_url_content(url):
    try:
        # 构造发送请求
        request = urllib.request.Request(url)
        request.add_header('Referer', url)
        # 发出请求并取得响应
        response = urllib.request.urlopen(request)
    except urllib.request.HTTPError as err:
        if err.getcode() != 200:
            return "404"
    # 获取网页内容
    html = response.read()
    # 返回网页内容
    return html

def get_url_detail(url):
    try:
        # 构造发送请求
        request = urllib.request.Request(url)
        # 发出请求并取得响应
        response = urllib.request.urlopen(request)
    except urllib.request.HTTPError as err:
        if err.getcode() != 200:
            return "404"
    # 获取网页内容
    html = response.read()
    # 返回网页内容
    return html


# 通过BeautifulSoup解析后的结构来获取内容，并存入excel
# 注意，因为不同的网页结构不同，爬取其他网页时，只需要改动这里的内容就可以了，其他东西不用改(main方法里的某些地方还是要改动，但主题思想不变)
# 存入excel也是这里的特定操作，当然后面也可以选择存入数据库或者是缓存
def parser_to_excel(soup):

    global num
    # 查看网页可以看到我们要获取的信息都在class='grid_view'里面，所以获取到它，再获取到其中所有的li标签，组成一个list
    content_list = soup.find(class_='interest-list').find_all('li')
    # 循环li标签列表
    for book_item in content_list:
        # 因为通过查看网页，可以看见一个图书节点的前两个a标签，第一个是图片链接，第二个是名称链接
        # 获取图书的详情url
        book_detail_url = book_item.find_all('a')[0].get('href')
        print("book_detail_url "+book_detail_url)
        # 获取图书详情页面的信息并解析
        book_detail_content = get_url_detail(book_detail_url)
        list_book_detail = list()  # 存储每本图书的详细信息
        if book_detail_content == "404":
            continue
        else:
            urlSetTemp[num].add(book_detail_url)  # 将图书的url存在urlSet中
            book_detail_soup = BeautifulSoup(book_detail_content, 'html.parser')
            title = book_detail_soup.find(id='mainpic').find_all('a')[0].get('title')
            list_book_detail.append(title)
            #sheet.write(n, 0, title)
            book_detail = book_detail_soup.find(id='info').find_all("span", "pl")
            # count_col = 1
            for span_item in book_detail:
                tag_name = span_item.next_element
                if str(tag_name)[-1] != ":":
                    tag_name = str(tag_name) + ":"  # 如果标签（页数，出版社，作者）之后没有":"，则加上":"
                tag_content = ''  # 存储标签对应的内容
                if span_item.find_next_sibling().name == "a":
                    i = 0
                    for item in span_item.find_next_siblings("a"):  # 防止有多个<a>标签的情况
                        if i != len(span_item.find_next_siblings("a")) - 1:  # 如果不是最后一个元素，则需要在元素后加","用于分隔内容
                            tag_content = "".join(tag_content + item.text) + ","
                        else:
                            tag_content = "".join(tag_content + item.text)
                        i += 1
                        # "".join(str(tag_content).split())的意思是去除tag_content中的所有的空格，回车换行符
                    print("输出为 " + str(tag_name) + "".join(str(tag_content).split()))
                    list_book_detail.append(str(tag_name) + "".join(str(tag_content).split()))
                    #sheet.write(n, count_col, str(tag_name) + "".join(str(tag_content).split()))
                else:
                    tag_content = span_item.next_sibling
                    print("输出为 " + tag_name + tag_content)
                    list_book_detail.append(tag_name + tag_content)  # 存储某本书的所有详细信息
                    #sheet.write(n, count_col, tag_name + tag_content)
                # count_col += 1
            # print("正往第" + str(n) + "行写入数据")
            # 每次循环完，行数+1

            infoDictTemp[num][book_detail_url] = list_book_detail

if __name__ == "__main__":
    # 设置爬取的初始url
    base_url = 'https://book.douban.com'
    # 要爬取的图书信息的首页
    list_visit_url = ['https://book.douban.com/people/154001100/collect?sort=time&start=0&mode=grid&tags_sort=count',
                      'https://book.douban.com/people/138083612/collect?sort=time&start=0&mode=grid&tags_sort=count']

    # index = 0
    for tar_url in list_visit_url:
        # 获取初始化页面的内容
        content = get_url_content(tar_url)

        # 把内容解析成BeautifulSoup结构(BeautifulSoup的内容可以看下http://beautifulsoup.readthedocs.io/zh_CN/latest/)
        soup = BeautifulSoup(content, 'html.parser')

        # 获取当前页的信息并存入excel
        parser_to_excel(soup)

        # 获取其他要爬取的url地址
        # 可以通过按f12看到分页的代码写在class='paginator'里
        # 所以我们先获取到class=‘paginator’的div
        paginator_div = soup.find(class_='paginator')
        if paginator_div is not None:
            next_div = paginator_div.find(class_='next')
            if next_div.find_all('a'):
                link = next_div.find_all('a')[0]
                while link is not None:
                        # 因为href里都是"?start=25&amp;filter="这种形式，缺少网页前缀，所以拼接一下
                        other_url = base_url + link.get('href')

                        print("正在爬取url:" + other_url)

                        # 同上，获取到其他网页的内容
                        other_url_content = get_url_content(other_url)

                        # 同上，获取到内容后通过BeautifulSoup，解析
                        soup = BeautifulSoup(other_url_content, 'html.parser')

                        # 把分页里的2,3...等页里面的信息解析并存入excel
                        parser_to_excel(soup)
                        paginator_div = soup.find(class_='paginator')
                        next_div = paginator_div.find(class_='next')
                        if next_div.find_all('a'):
                            link = next_div.find_all('a')[0]
                        else:
                            break
        # 这里已经对某个人想读的书的url全部记录在一个set中，图书的详细信息已经存放在dict中，
        # 此时需要把这个set添加进urlSet_list中，把这个dict存储在infoDict_list，
        urlSet_list.append(urlSetTemp[num])
        # print(urlSet)
        print(urlSet_list)
        infoDict_list.append(infoDictTemp[num])
        num += 1
    # print("urlSet_list的长度 ")
    # print(len(urlSet_list))
    # print(urlSet_list[0])
    # print(urlSet_list[1])
    # print("urlSet_list ")
    # print(urlSet_list)
    # index += 1
    union_url = urlSet_list[0] & urlSet_list[1]  # 两位读者共有的图书的url
    # print(urlSet_list[0])
    # print(urlSet_list[1])
    if len(union_url) == 0:
        print("两位读者之间没有共同想读的书")
    else:

        book_Dict = infoDict_list[0]
        for common_url in union_url:
            count_col = 0
            comm_info = book_Dict.get(common_url)
            for info in comm_info:
                sheet.write(n, count_col, info)
                count_col += 1
            n += 1


    # 保存
    book.save('张三和李四读过的共同的图书.xls')
