import wx
import os
import PDF_content as pc


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''

        super(Mywin, self).__init__(parent, title=title,size=(800,800))
        # A Statusbar in the bottom of the window
        self.CreateStatusBar()
        self.SetStatusText("生成PDF书签")




        # Setting up the menu. file menu
        file_menu = wx.Menu()
        file_menu_open = file_menu.Append(wx.ID_OPEN, "&选择文件", " 选择文件")
        file_menu_about = file_menu.Append(wx.ID_ABOUT, "&关于", " 由sweeney_he制作")
        file_menu_exit = file_menu.Append(wx.ID_EXIT, "&退出", " 退出程序")




        # Setting up the menu. tool menu
        tool_menu = wx.Menu()
        tool_menu_auto = tool_menu.Append(wx.ID_FILE1, "&自动模式", " 输入目录位置,自动识别生成目录")
        tool_menu_manul = tool_menu.Append(wx.ID_FILE2, "&手动模式", " 已有目录数据,选择目录txt文件")


        # Creating the menubar
        menuBar = wx.MenuBar()
        #---file
        menuBar.Append(file_menu, "&文件")  # Adding the "filemenu" to the MenuBar
        #---tool
        menuBar.Append(tool_menu, "&模式")  # Adding the "filemenu" to the MenuBar

        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.






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



        """"=============页面偏移选择区域============="""
        nm = wx.StaticBox(panel, -1, '信息与确认:')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        fn = wx.StaticText(panel, -1, " 目录与实际PDF页数偏移: ")

        nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 2)
        self.offset = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(50,25))
        run_button  = wx.Button(panel, -1, '运行')

        nmbox.Add(self.offset, 0, wx.ALL | wx.CENTER,  10)
        nmbox.Add(run_button, 0, wx.ALL | wx.CENTER, 10)
        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 10)



        """"=============PDF路径选择区域============="""
        sbox1 = wx.StaticBox(panel, -1, '选择PDF:')
        sbox1Sizer = wx.StaticBoxSizer(sbox1, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.pdf_path_text = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(600,25))

        hbox.Add(self.pdf_path_text, 0, wx.ALL | wx.LEFT, 10)
        chooseFile_button1 = wx.Button(panel, -1, '选择文件')

        hbox.Add(chooseFile_button1, 0, wx.ALL | wx.LEFT, 10)

        sbox1Sizer.Add(hbox, 0, wx.ALL | wx.LEFT, 10)





        """"=============txt目录文件路径选择区域============="""
        sbox2 = wx.StaticBox(panel, -1, '选择目录文件(txt格式):')
        sbox2Sizer = wx.StaticBoxSizer(sbox2, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_path_text = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT,size=(600,25))

        hbox.Add(self.txt_path_text, 0, wx.ALL | wx.LEFT, 10)
        chooseFile_button2 = wx.Button(panel, -1, '选择文件')

        hbox.Add(chooseFile_button2, 0, wx.ALL | wx.LEFT, 10)

        sbox2Sizer.Add(hbox, 0, wx.ALL | wx.LEFT, 10)


        """===================目录编辑区域==================="""
        textbox = wx.StaticBox(panel, -1, '选择目录文件(txt格式):')
        textboxSizer = wx.StaticBoxSizer(textbox, wx.VERTICAL)

        text_in_box = wx.BoxSizer(wx.HORIZONTAL)
        #编辑区域
        self.txt_content_area = wx.TextCtrl(panel, -1,style=wx.TE_MULTILINE | wx.ALIGN_LEFT,  size=(800, 600))
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, '微软雅黑')
        self.txt_content_area.SetFont(font)

        text_in_box.Add(self.txt_content_area, 0, wx.ALL | wx.LEFT, 1)
        textboxSizer.Add(text_in_box, 0, wx.ALL | wx.LEFT, 1)



        #sbox1Sizer、sbox2Sizer加入vbox排版器
        vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)
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
        self.Bind(wx.EVT_MENU, self.on_tool_menu_auto, tool_menu_auto)
        self.Bind(wx.EVT_MENU, self.on_tool_menu_manul, tool_menu_manul)

        # 选择文件按钮绑定
        self.Bind(wx.EVT_BUTTON, self.on_chooseFile_button1, chooseFile_button1)
        self.Bind(wx.EVT_BUTTON, self.on_chooseFile_button2, chooseFile_button2)
        #运行按钮绑定
        self.Bind(wx.EVT_BUTTON,self.on_runButton,run_button)




        self.Show()















#事件响应函数
    #file菜单
    def OnAbout(self, e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, "SWEENEY HE ©copyright \n  2021年01月09日", "关于作者", wx.OK)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.

    def OnOpen(self, e):
        pass
        """ Open a file"""
        # filesFilter = "All files (*.*)|*.*"
        filesFilter = "PDF (*.pdf)|*.pdf|" "txt (*.txt*)|*.txt*"
        # fileDialog = wx.FileDialog(self, message ="选择单个文件", wildcard = filesFilter, style = wx.FD_OPEN)

        dlg = wx.FileDialog(self, "选择文件", wildcard = filesFilter, style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname, self.filename)
            self.path_text.SetValue(path)

            # f = open(os.path.join(self.dirname, self.filename), 'r')
            # self.control.SetValue(f.read())
            # f.close()

        dlg.Destroy()

    #tool菜单
    def on_tool_menu_auto(self):
        pass

    def on_tool_menu_manul(self):
        pass




    #按钮区
    #pdf路径选择
    def on_chooseFile_button1(self,event):
        filesFilter = "PDF (*.pdf)|*.pdf"

        dlg = wx.FileDialog(self, "选择文件", wildcard=filesFilter, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname, self.filename)
            self.pdf_path_text.SetValue(path)

        dlg.Destroy()

    #txt文件路径选择
    def on_chooseFile_button2(self,event):
        filesFilter = "txt (*.txt*)|*.txt*"
        dlg = wx.FileDialog(self, "选择文件", wildcard=filesFilter, style=wx.FD_OPEN)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
        else:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname, self.filename)
            self.txt_path_text.SetValue(path)
            content = ""
            with open(path,"r",encoding="utf-8") as contentFile:
                for line in contentFile.readlines():
                    content+=str(line)
                self.txt_content_area.SetValue(content)

    #on_runButton运行按钮
    def on_runButton(self,event):
        #获取页面偏移
        offset = self.offset.GetValue()
        #验证页面偏移
        if not is_number(offset):
            dlg = wx.MessageDialog(self, "页面偏移必须是数字\n请重新输入", "⚠输入出错", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
            return
        #获取txt路径
        txt_path = self.txt_path_text.GetValue()
        #获取pdf路径
        pdf_path = self.pdf_path_text.GetValue()
        #运行pdf添加程序
        print(pc.addBookmark(pdf_path, txt_path, int(offset)))

        # try:
        # except Exception as e:
        #     dlg = wx.MessageDialog(self, "程序运行出现异常\n{}:".format(e), "⚠运行出错", wx.OK)
        #     dlg.ShowModal()  # Shows it
        #     dlg.Destroy()  # finally destroy it when finished.
        # else:
        #     dlg = wx.MessageDialog(self, "添加书签成功!文件位置:\n{}:".format(pdf_path), "运行完成", wx.OK)
        #     dlg.ShowModal()  # Shows it
        #     dlg.Destroy()  # finally destroy it when finished.





app = wx.App()
Mywin(None, 'PDF书签制作')
app.MainLoop()

