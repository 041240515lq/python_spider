# python_spider 
程序运行要求：需要在用户的pc机上安装python3.0及以上版本，并配置好环境变量。

需要安装一下三个库，打开cmd窗口运行：

安装pip,运行命令python -m pip install -U pip

安装beautifulSoup库,运行命令pip install beautifulSoup4

安装xlwt库，运行命令pip install xlwt

文件中有两个脚本程序：spiderBook.py和outputCommonWantBook.py。

一.脚本spiderBook.py的功能是爬取某个用户在豆瓣上标记的想读或者读过的图书信息。
用户运行需要将代码中的变量first_url的值设置为目标用户在豆瓣上标记的想读或者已读的图书的首页的url。如果需要修改程序运行后生成的excel文件的名字，
需要修改saveName的值。例如我在豆瓣上想读的图书的首页url为“https://book.douban.com/people/154001100/collect?sort=time&start=0&mode=grid&tags_sort=count”
可以通过IDE运行脚本，如果通过命令行运行，通过cmd命令打开窗口，输入“python python脚本在你的pc机上的位置”，按回车键就可以运行。
命令行运行示例：python D:\workspaces\python_spider\spiderDouban\spiderBook.py

二.脚本outputCommonWantBook.py的功能是得到任意两个用户在豆瓣上标记的想读或者已读的图书的信息的交集。
用户运行程序时需要将代码中的变量list_visit_url的值设置为为两个目标用户在豆瓣上标记的图书的信息的首页的url。如果需要修改程序运行后生成的excel文件的名字，
需要修改saveName的值。运行过程参见上个脚本的运行过程。

代码运行生成的excel文件会存储在和两个脚本同级的目录下。
