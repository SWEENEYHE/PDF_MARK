"""爬虫类源文件"""

import requests
import re
import time
import random
from lxml import etree

#来源1:中国图书网
  #1.搜索：http://www.bookschina.com/book_find2/?stp=关键字&sCate=0
  #2.列表：//div[@class='bookList']/ul/li[1]/div[@class='infor']/h2[@class='name']/a/@href
  #3.详细页:http://www.bookschina.com/7411843.htm
    #//div[@id='catalogSwitch']
#来源2：0000000000



    #爬取目录类
class ContentSpider:

    def __init__(self,queue,abortQueue):
        self.header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
                     ,"Referer":"http://www.china-pub.com/"
                     ,"Cookie":"ASP.NET_SessionId=0qtky345gh1zr445gsgln345"}
        #同步用队列
        self.queue = queue
        #终止队列
        self.abortQueue = abortQueue

    #更新终止标志
    def updateAbort(self):
        #只要不空就判断为终止
        if not self.abortQueue.empty():
            return True

    #提取搜索页面中所有商品链接
    def getUrl(self,html):
        htmlElem = etree.HTML(html)
        t = htmlElem.xpath("//li[@class='result_name']/a/@href")
        # 需要的结果：http://product.china-pub.com/4736113
        # 爬取内容会掺入少量无效url，利用条件丢弃
        out=[]
        for temp in t:
            temp = temp.split("/")
            if len(temp)==4:
                out.append(temp[len(temp)-1])
        # print("t:")
        # print(out)
        return out

    # #删除textarea标签
    def removeDiv(self, html):
        html = re.sub('<div id="ml_txt" style="display:none;">', "", html)  # HTML标签
        return html


    #提取目录信息
    def getContent(self,productId,num):
        # #构造详细信息url
        url = "http://product.china-pub.com/{}".format(productId)
        # # #获取详细页面json数据
        response = requests.get(url,headers=self.header)
        try:
            self.html = response.content.decode(encoding="gbk")
            # self.html = response.text
        except Exception:
            try:
                self.html = response.content.decode(encoding="utf-8")
            except Exception:
                return 0

        # print(response.text)


        # with open("../detail.html","r",encoding="utf-8") as htmlFile:
        #     self.html=htmlFile.readlines()
        # self.html = "".join(self.html)
        # print("html:"+self.html)


        #xpath获取目录信息
        t = self.removeDiv(self.html)
        #保存剔除div标签后的内容用于测试
        # with open("../test1.html","w",encoding="utf-8") as testHtml:
        #     testHtml.write(t)
        htmlElem1 = etree.HTML(t)
        try:
            self.t = htmlElem1.xpath("//h3[@id='ml']/../div/text()")
        except Exception:
            pass

        #获取书籍标题用于显示在第1行
        bookTitle = ""
        try:
            bookTitle = htmlElem1.xpath("//div[@class='pro_book']/div[@class='pro_book']/h1/text()")
        # print(self.t)
        except Exception:
            pass


        #将目录转换成字符串,清除空行
        out = ""
        for i in self.t:
            out+=i.strip()+"\n"
        #如果总目录长度小于10，则丢弃
        if len(out)<10:
            return 0
        # 判断标题,将标题写到文件第1行
        #并将标题展示到进度信息中
        bookTitle = "《"+"".join(bookTitle).strip()+"》  0"+'\n'
        if len(bookTitle) > 1:
            out = bookTitle+out
            self.queue.put(bookTitle)
        # print(bookTitle)

        #将目录写到文件中
        with open("./contents/content-{}.txt".format(num), "w", encoding="utf-8") as afterHtml:
            afterHtml.write(out)
        return 1


    #提取商品编号
    def getProductId(self,url):
        #除了数字全部删除
        return re.sub("[^0-9]+","",url)


    #主流程控制
    def run(self,startUrl,key):
        # #url编码
        # key = urllib.parse.quote(key)
        #中文设置gbk编码
        key = key.encode("gbk")
        #设置初始参数
        p = {"key1":key}
        response = requests.get(startUrl,params=p,headers=self.header)
        #防止页面通过js重定向，再次请求
        if len(response.text)<200:
            response = requests.get(startUrl, params=p, headers=self.header)
        # print(response.status_code)
        # print(response.url)
        # print(response.request.headers)
        # print(response.text)


        #从中间搜索页面提取链接
        urls = self.getUrl(response.content)
        # print(urls)
        #多个url只要有一个提取目录成功则成功
        out=0
        for url in urls:
            # 判断终止
            if self.updateAbort():
                return out
            # print("out1:"+str(out))
            #提取商品编号
            # productId = self.getProductId(url)
            #通用性处理，保留url
            productId = url
            # print(productId)
            #随机停止500ms-1000ms防止反爬虫机制
            time.sleep(random.randint(5,10)*0.1)
            #获取目录状态,目录信息已经保存在txt中
            # print("id: "+productId)
            out = out+self.getContent(productId,out+1)
            # print("out2:"+str(out))



        #同步队列标志结束
        self.queue.put("_OVER_")
        self.queue.task_done()
        return out






# spider = ContentSpider()
# spider.run("http://search.china-pub.com/s/?","故宫秘境文丛·倦勤")
