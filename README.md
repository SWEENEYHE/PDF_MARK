### 直接使用党：dist下的PDF_MARKER文件夹是可以直接使用的.exe源，注意需要整个文件夹一起下载
### 使用pychrome开发，所有工具方法/类都作为第三方包导入，因此修改源文件无效，需要修改site-packages中的代码

### 打包命令,使用第三方模块必须指定路径(windows下生成exe需要安装pyinstaller)
````
pyinstaller -D -w -i "pdf.ico"  PDF_MARKER.py  -p C:\Users\SWEENEY_HE\PycharmProjects\PDF_MARKER_FINAL\venv\Lib\site-packages
````
使用说明
````
author:sweeneyhe
descreption: a tool to add contents/Catalogue/bookmark to a pdf
````

[my csdn blog](https://blog.csdn.net/SWEENEY_HE/article/details/105574290?spm=1001.2014.3001.5502)

#### 1.手动模式：自行编辑目录结构txt文件

>使用一个txt文件，内容如下:每行写一个索引，前面写索引名，后面写pdf中的实际页码。行与行之间按照目录级别进行缩进，同级目录缩进相同。每行后面使用任意大于一个空格或者制表符接页码
>![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417101944187.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70)
>可以使用OCR(可以使用Adobe Acr0bat DC软件等)将原文目录转成文档，自行缩进编辑成txt，代码自动去除各种符号
>![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417121853763.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70)
>识别+手动缩进+数字改正后的效果
>![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417123158715.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70)
>最终效果:
>![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417123321690.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70)

##### 注意：必须填写偏移，偏移是指txt目录文件中的页码与实际PDF所在页面的页码的差值，允许为负数,自行使用pdf阅读工具打开pdf，对照pdf真实页码与目录页码

#### 2.自动获取模式：输入ISBN/书籍名在线获取

​	自动获取基于爬虫爬取目录，由于只爬取了一个网站，书籍可能不全，不一定能够获得对应书籍的目录，尽量使用ISBN获取更为准确。也可以自己上当当等网站手动复制目录。 使用Notepad++等软件进行编辑可以多选缩进。

自动获取的目录存在于选择目录文件所示的路径中，文件名为content-数字.txt，点击**选择目录**默认打开的就是获取到的目录文件路径。如果不是，自行复制路径打开即可。

![自动模式预览](https://img-blog.csdnimg.cn/2021022315250221.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70#pic_center)

#### 3.导出目录功能

![导出目录预览](https://img-blog.csdnimg.cn/20210223152528301.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NXRUVORVlfSEU=,size_16,color_FFFFFF,t_70#pic_center)

​	导出pdf的目录为txt格式，即逆操作。操作步骤：

​		1.先选择PDF文件，

​		2.文件->导出目录

​		3.如果导出成功，默认txt文件在pdf所在路径下

#### 4.bug提示

##### （1）未响应：

由于添加目录懒得做多线程，所以点击运行后大的pdf可能会卡顿，最好不要动鼠标，因为窗口和添加目录的处理过程在同一线程，否则会出现未响应等情况，出现了也没关系，选择等待响应等一会就好了。

##### （2）添加失败：

​    PYPDF2的问题。详细解决方法参考提示窗口，主要原因是已经用其他软件添加过目录，如果在其他软件中删除所有目录还是不行的话。目前已知的解决方式是：使用Adobe Acrobat Pro DC等软件将原PDF文件进行优化还是压缩其中一个，生成一个新的PDF文件。

