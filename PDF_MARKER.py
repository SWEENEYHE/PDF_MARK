import wx
import os
import shutil
import threading
import queue
import time
import win32api
#pdf导出目录模块
from dpendencies import exportPdfMark as em, Myspider as spider, PDF_content as pc

#爬虫模块


"""
主流程文件
其他工具代码都作为第三方包引入，所以真正运行的代码在site-packages中，dependcies中的源代码实际不运行
"""

#线程类
class MyThread(threading.Thread):
    def __init__(self,key,queue,abortQueue):
        threading.Thread.__init__(self)
        #关键字
        self.key = key
        #与主程通讯队列
        self.queue = queue
        #终止爬虫线程队列
        self.abortQueue = abortQueue
        #返回目录结果数，0表示获取失败
        self.result=0
        #启动线程
        self.start()

    #线程函数
    def run(self):
        # 实例化爬虫类
        contentSpider = spider.ContentSpider(self.queue,self.abortQueue)
        self.result = contentSpider.run("http://search.china-pub.com/s/?", self.key)
    #获取返回值
    def getResult(self):
        return self.result

#工具类
class Utils:
    def __init__(self):
        pass

    @staticmethod
    def is_number(s):
        try:
           int(s)
           return True
        except (TypeError, ValueError):
            pass
        return False

    #创建文件夹
    @staticmethod
    def mkdir(path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)





#绘制图形类
class Mywin(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        #队列用于线程间传递消息
        self.queue = queue.Queue()
        #终止消息队列用于线程间传递终止消息
        self.abortQueue = queue.Queue()
        #保存目录数量
        self.result = 0
        super(Mywin, self).__init__(parent, title=title,size=(800,800))
        # A Statusbar in the bottom of the window
        self.CreateStatusBar()
        self.SetStatusText(u"生成PDF书签")

        # 用于从module中读取ico，避免了要在程序所在路径附上此ico
        exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Setting up the menu. file menu
        file_menu = wx.Menu()
        file_menu_open = file_menu.Append(wx.ID_OPEN, u"&导出目录", " 导出含目录PDF中的目录为txt格式")
        file_menu_about = file_menu.Append(wx.ID_ABOUT, u"&关于", " 由sweeney_he制作")
        file_menu_exit = file_menu.Append(wx.ID_EXIT, u"&退出", " 退出程序")




        # # Setting up the menu. tool menu
        # self.tool_menu = wx.Menu()
        # tool_menu_auto = tool_menu.Append(wx.ID_FILE1, u"&自动模式", " 输入目录位置,自动识别生成目录")
        # tool_menu_manul = tool_menu.Append(wx.ID_FILE2, u"&手动模式", " 已有目录数据,选择目录txt文件")


        # Creating the menubar
        self.menuBar = wx.MenuBar()
        #---file
        self.menuBar.Append(file_menu, u"&文件")  # Adding the "filemenu" to the MenuBar
        # #---tool
        # self.menuBar.Append(self.tool_menu, u"&已获取目录")  # Adding the "filemenu" to the MenuBar

        self.SetMenuBar(self.menuBar)  # Adding the MenuBar to the Frame content.






        #面板
        panel = wx.Panel(self)
        #总体排版器
        vbox = wx.BoxSizer(wx.VERTICAL)

        # #页面范围布局
        # nm = wx.StaticBox(panel, -1, 'PDF中目录所在页的范围:')
        # nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)
        #
        # nmbox = wx.BoxSizer(wx.HORIZONTAL)
        # fn = wx.StaticText(panel, -1, "真实页数:  ")
        #
        # nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 2)
        # nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(50,25))
        # nm2 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(50,25))
        # ln = wx.StaticText(panel, -1, "—")
        #
        # nmbox.Add(nm1, 0, wx.ALL | wx.CENTER, 2)
        # nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 2)
        # nmbox.Add(nm2, 0, wx.ALL | wx.CENTER, 2)
        # nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 20)

        #第一层并列两个区域
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        """"=============页面偏移选择区域============="""
        nm1 = wx.StaticBox(panel, -1, u'信息与确认:')
        nmSizer1 = wx.StaticBoxSizer(nm1, wx.VERTICAL)

        nmbox1 = wx.BoxSizer(wx.HORIZONTAL)
        fn1 = wx.StaticText(panel, -1, u" 目录与实际PDF页数偏移: ")

        nmbox1.Add(fn1, 0, wx.ALL | wx.CENTER, 2)
        self.offset = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(50,25))
        run_button  = wx.Button(panel, -1, u'运行')

        nmbox1.Add(self.offset, 0, wx.ALL | wx.CENTER,  10)
        nmbox1.Add(run_button, 0, wx.ALL | wx.CENTER, 10)
        nmSizer1.Add(nmbox1, 0, wx.ALL | wx.CENTER, 10)

        """"=============在线搜索目录区域============="""
        nm2 = wx.StaticBox(panel, -1, u'在线搜索目录:')
        numSizer2 = wx.StaticBoxSizer(nm2, wx.VERTICAL)

        nmbox2 = wx.BoxSizer(wx.HORIZONTAL)
        fn2 = wx.StaticText(panel, -1, u" 书籍ISBN/名称: ")

        nmbox2.Add(fn2, 0, wx.ALL | wx.CENTER, 2)
        self.isbn_area = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT, size=(170, 25))
        search_button = wx.Button(panel, -1, u'搜索')

        nmbox2.Add(self.isbn_area, 0, wx.ALL | wx.CENTER, 10)
        nmbox2.Add(search_button, 0, wx.ALL | wx.CENTER, 10)
        numSizer2.Add(nmbox2, 0, wx.ALL | wx.CENTER, 10)

        topSizer.Add(nmSizer1,0,wx.ALL,2)
        topSizer.Add(numSizer2,0,wx.ALL,2)






        """"=============PDF路径选择区域============="""
        sbox1 = wx.StaticBox(panel, -1, u'选择PDF:')
        sbox1Sizer = wx.StaticBoxSizer(sbox1, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.pdf_path_text = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(610,25))

        hbox.Add(self.pdf_path_text, 0, wx.ALL | wx.CENTER, 10)
        chooseFile_button1 = wx.Button(panel, -1, u'选择PDF')

        hbox.Add(chooseFile_button1, 0, wx.ALL | wx.CENTER, 10)

        sbox1Sizer.Add(hbox, 0, wx.ALL | wx.CENTER, 10)





        """"=============txt目录文件路径选择区域============="""
        sbox2 = wx.StaticBox(panel, -1, u'选择目录文件(txt格式):')
        sbox2Sizer = wx.StaticBoxSizer(sbox2, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_path_text = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(610,25))

        hbox.Add(self.txt_path_text, 0, wx.ALL | wx.CENTER, 10)
        chooseFile_button2 = wx.Button(panel, -1, u'选择目录')

        hbox.Add(chooseFile_button2, 0, wx.ALL | wx.CENTER, 10)

        sbox2Sizer.Add(hbox, 0, wx.ALL | wx.CENTER, 10)


        """===================目录编辑区域==================="""
        textbox = wx.StaticBox(panel, -1, u'编辑目录(自动同步到原TXT中):')
        textboxSizer = wx.StaticBoxSizer(textbox, wx.VERTICAL)

        text_in_box = wx.BoxSizer(wx.HORIZONTAL)
        #编辑区域
        self.txt_content_area = wx.TextCtrl(panel, -1,style=wx.TE_MULTILINE | wx.ALIGN_LEFT,  size=(2000, 600))
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'微软雅黑')
        self.txt_content_area.SetFont(font)

        text_in_box.Add(self.txt_content_area, 0, wx.ALL | wx.LEFT, 1)
        textboxSizer.Add(text_in_box, 0, wx.ALL | wx.LEFT, 1)



        #sbox1Sizer、sbox2Sizer加入vbox排版器
        vbox.Add(topSizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(sbox1Sizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(sbox2Sizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(textboxSizer,0,wx.ALL | wx.CENTER, 5)


        #panel设置排版器
        panel.SetSizer(vbox)

        #收尾工作
        self.Centre()
        panel.Fit()

        """"=================绑定事件区域=================="""
        # files menu bind Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, file_menu_open)
        self.Bind(wx.EVT_MENU, self.OnExit, file_menu_exit)
        self.Bind(wx.EVT_MENU, self.OnAbout, file_menu_about)

        # tools menu bind Events
        # self.Bind(wx.EVT_MENU, self.on_tool_menu_auto, self.tool_menu_auto)
        # self.Bind(wx.EVT_MENU, self.on_tool_menu_manul, self.tool_menu_manul)

        # 选择文件按钮绑定
        self.Bind(wx.EVT_BUTTON, self.on_chooseFile_button1, chooseFile_button1)
        self.Bind(wx.EVT_BUTTON, self.on_chooseFile_button2, chooseFile_button2)

        #运行按钮绑定
        self.Bind(wx.EVT_BUTTON,self.on_runButton,run_button)

        # 搜索目录按钮
        self.Bind(wx.EVT_BUTTON, self.on_search_button, search_button)

        #编辑区域失去焦点绑定
        #注意这种非命令事件的绑定方法
        self.txt_content_area.Bind(wx.EVT_KILL_FOCUS,self.onKillFocus)
        #self.txt_content_area.Bind(wx.EVT_SET_FOCUS,self.onGetFocus)




        self.Show()












#事件响应函数
    #file菜单
    def OnAbout(self, e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, "MY CSDN BLOG: https://blog.csdn.net/SWEENEY_HE  \n  2021年01月09日", u"关于作者", wx.OK)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.

    def OnOpen(self, e):
        #先判断PDF路径
        # 获取pdf路径
        pdfPath = self.pdf_path_text.GetValue()
        print(pdfPath)
        if not os.path.exists(pdfPath):
            self.showDialog("请先在主页面选择PDF文件||选择的PDF文件不存在","提示")
            return
        # filesFilter = "All files (*.*)|*.*"
        filesFilter = "txt (*.txt*)|*.txt*"
        # fileDialog = wx.FileDialog(self, message ="选择单个文件", wildcard = filesFilter, style = wx.FD_OPEN)

        dlg = wx.FileDialog(self, u"保存目录文件为：", wildcard = filesFilter, style = wx.FD_SAVE)
        index = str.rfind(pdfPath,"\\")
        txtfilename = pdfPath[index+1:]+".txt"

        dlg.SetFilename(txtfilename)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            path = os.path.join(dirname, filename)
            #print(path)
            result = em.extractBookmark(pdfPath, path)
            self.showDialog(result,"提示")



        dlg.Destroy()

    #tool菜单
    def on_tool_menu_auto(self):
        pass

    def on_tool_menu_manul(self):
        pass


    #下拉列表函数
    def on_content(self,event,i):
        content=""
        with open("./contents/content-{}".format(i), "r", encoding="utf-8") as contentFile:
            for line in contentFile.readlines():
                content += str(line)
        self.txt_content_area.SetValue(content)






    #按钮区
    #pdf路径选择
    def on_chooseFile_button1(self,event):
        filesFilter = "PDF (*.pdf)|*.pdf"

        dlg = wx.FileDialog(self, u"选择文件", wildcard=filesFilter, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname, self.filename)
            self.pdf_path_text.SetValue(path)

        dlg.Destroy()

    #txt文件路径选择
    def on_chooseFile_button2(self,event):
        filesFilter = "txt (*.txt*)|*.txt*"
        #选择文件，默认路径为获取到的目录路径
        dlg = wx.FileDialog(self, u"选择文件", wildcard=filesFilter, style=wx.FD_OPEN,defaultDir=os.getcwd()+"\contents")
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
        else:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname, self.filename)

            self.txt_path_text.SetValue(path)
            with open(path, 'r',encoding="utf-8") as f:
                #self.txt_content_area.write(out)
                self.txt_content_area. SetValue("".join(f.readlines()))




    def onGetFocus(self,event):
        txtpath = self.txt_path_text.GetValue()
        if not os.path.exists(txtpath):
            self.showDialog("文件不存在，请选择正确文件后再编辑", "提示")

            #event.Skip()

            return


    #txt失去焦点
    def onKillFocus(self,event):
        txtpath = self.txt_path_text.GetValue()

        #将content内容写回txt文件
        content = self.txt_content_area.GetValue()

        if not os.path.exists(txtpath):
            self.showDialog("目录文件不存在，请选择正确的文件后再编辑", "提示")
        else:
            with open(txtpath, "w", encoding="utf-8") as textFile:
                textFile.write(content)
        event.Skip()





    #on_runButton运行按钮
    def on_runButton(self,event):
        #获取页面偏移
        offset = self.offset.GetValue()
        #验证页面偏移
        if not Utils.is_number(offset):
            dlg = wx.MessageDialog(self, u"页面偏移必须是整数(包括正负)\n请重新输入", "输入出错", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
            return
        #获取txt路径
        txt_path = self.txt_path_text.GetValue()

        #获取pdf路径
        pdf_path = self.pdf_path_text.GetValue()


        #运行pdf添加程序
        try:
            print(pc.addBookmark(pdf_path, txt_path, int(offset)))
        except Exception as e:
            dlg = wx.MessageDialog(self, u"程序运行出现异常\n{}\n异常出现原因：\n1.[range] 书签数值+偏移值超出PDF实际页数范围\n2.[not in list] PDF本身使用其他软件制作过书签，请删除所有书签后重试\n3.[not find object等其他异常] PDF存在问题，请使用PDF软件转换优化压缩等手段处理后重试".format(e), u"⚠运行出错", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
        else:
            dlg = wx.MessageDialog(self, u"添加书签成功!文件位置:\n{}-new.pdf:".format(pdf_path.split(".")[0]), u"运行完成", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.

    #搜索目录按钮
    def on_search_button(self,event):
        #删除上次获取的目录
        shutil.rmtree("./contents")
        #重新创建新的目录
        Utils.mkdir("contents")
        # 获取要搜索的键ISBN/书名
        key = self.isbn_area.GetValue()
        # print("key"+key)

        #启动爬虫线程
        myThread = MyThread(key,self.queue,self.abortQueue)


        # print("main main main------------")
        #显示进度条
        success = self.showProcessBar()
        # 必须等待线程完成否则返回值还没有赋值,必为初值0
        myThread.join()
        self.result = myThread.getResult()

        # status = 1
        #爬取目录，生成为content-n.txt文件,n为1,2,3...返回值为n
        #爬取失败
        if not success or self.result<=0:
            self.showDialog("获取目录失败-解决办法或原因:\n1.输入ISBN获取\n2.获取过于频繁,被来源禁止请以后再试\n3.暂无目录","获取目录失败")
            return
        #爬取成功
        else:
            with open("./contents/content-1.txt","r",encoding="utf-8") as contentFile:
                content = contentFile.readlines()
            content = "".join(content)
            self.txt_content_area.SetValue(content)
            self.showDialog("获取目录成功\n共获取到目录{}条".format(self.result),"获取目录成功")
            #设置文件栏地址
            self.txt_path_text.SetValue(os.getcwd()+"\contents\content-1.txt")

            # content_menu = []
            #获取目录的简要信息
            #将目录列表加载到下拉菜单中
            # self.tool_menu = wx.Menu()
            # for i in range(1,self.result+1):
            #     with open("contents/content-{}.txt".format(i),"r",encoding="utf-8") as file:
            #         bookProfile = file.readline(128)
            #     print(bookProfile)
            #     content_menu.append(self.tool_menu.Append(wx.ID_FILE1, u"&目录{}".format(i), bookProfile))
            #     print("content_menu:",end=": ")
            #     print(content_menu[i-1])
            # '''''===========================这里有bug============================='''
            # ''''
            # self.Bind(wx.EVT_MENU, lambda e, mark=i: self.on_content(e, mark), self.content_menu[i])
            # AttributeError: 'Mywin' object has no attribute 'content_menu'
            # '''
            # #给bind回调函数传参数，利用lambda
            # self.content_menu[i-1].Bind(wx.EVT_MENU, lambda e, mark=i: self.on_content(e, mark))

             #重新设置menubar
            # self.SetMenuBar(self.menuBar)


    '''======================通用模块封装函数======================'''
    #显示对话框
    def showDialog(self,text,title):
        dlg = wx.MessageDialog(self,text,title,wx.OK)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.

    # 进度条
    def showProcessBar(self,progressMax=60):
        msg = "正在获取目录..."
        dlg = wx.ProgressDialog("获取进度", msg, progressMax,
                                   style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        keepGoing = True
        cancel = False
        success = False
        #用于用户终止时判断是否爬取成功
        flag = False
        count = 0

        while keepGoing  and count < progressMax:
            count = count + 1
            wx.Sleep(1)
            #从队列中取值
            if not self.queue.empty():
                msg = self.queue.get()
                flag = True
            #如果结束
            if msg=='_OVER_':
                # 更新进度条状态
                for t in range(count,progressMax):
                    dlg.Update(t, '搜索完成')
                    time.sleep(0.01)
                success = True
                break


            keepGoing = dlg.Update(count,msg)
            cancel = dlg.WasCancelled()
            #如果点击终止按钮
            if cancel==True:
                # print("点击取消")
                success = flag
                #终止爬虫线程
                self.abortQueue.put(1)
                break


            #剩余1s始终不结束
            if count >= progressMax:
                count = progressMax - 1



        #等待queue结束任务
        # self.queue.join()
        dlg.Destroy()
        #判断是否正常结束
        return success





if __name__ == "__main__":
    app = wx.App()
    # 创建一个目录文件夹
    Utils.mkdir("contents")
    Mywin(None, u'PDF书签制作')
    app.MainLoop()

