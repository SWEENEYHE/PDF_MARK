### 使用pychrome开发，所有工具方法/类都作为第三方包导入，因此修改源文件无效，需要修改site-packages中的代码

### 打包命令,使用第三方模块必须指定路径(windows下生成exe需要安装pyinstaller)
````
pyinstaller -D -w -i "pdf.ico"  PDF_MARKER.py  -p C:\Users\SWEENEY_HE\PycharmProjects\PDF_MARKER_FINAL\venv\Lib\site-packages
````