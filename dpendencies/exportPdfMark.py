
""""导出目录方法源文件"""

import sys
import re
from distutils.version import LooseVersion
from os.path import exists
from PyPDF2 import PdfFileReader

is_python2 = LooseVersion(sys.version) < '3'


def _parse_outline_tree(outline_tree, level=0):
    """Return List[Tuple[level(int), page(int), title(str)]]"""
    ret = []
    for heading in outline_tree:
        if isinstance(heading, list):
            # contains sub-headings
            ret.extend(_parse_outline_tree(heading, level=level+1))
        else:
            ret.append((level, heading.page.idnum, heading.title))
    return ret

def extractBookmark(pdf_path, bookmark_txt_path):
    if not exists(pdf_path):
        return "Error: No such file: {}".format(pdf_path)
    if exists(bookmark_txt_path):
        print("Warning: Overwritting {}".format(bookmark_txt_path))

    reader = PdfFileReader(pdf_path)
    # List of ('Destination' objects) or ('Destination' object lists)
    #  [{'/Type': '/Fit', '/Title': u'heading', '/Page': IndirectObject(6, 0)}, ...]
    outlines = reader.outlines
    #print(outlines)
    # List[Tuple[level(int), page(int), title(str)]]
    outlines = _parse_outline_tree(outlines)
    max_length = max(len(item[-1]) + 2 * item[0] for item in outlines) + 1
    # print(outlines)


    with open(bookmark_txt_path, 'w',encoding="utf-8") as f:
        #prepage = 921
        #cur = 22
        for level, page, title in outlines:
            level_space = '\t' * level
            title_page_space = ' ' * (max_length - level * 2 - len(title))
            if is_python2:
                title = title.encode('utf-8')
            #某些pdf由于目录出错需要递推分析生成目录
            #page = cur
            #cur = cur+int((page-prepage)/3)
            #prepage = page;
            #某些目录title后有未知编码字符需要去除，否则wxpythontextarea显示不出
            rule=re.compile(r"[^a-zA-Z0-9（）【】\u4e00-\u9fa5]")
            title = title.strip()
            title = rule.sub('',title)
            #f.write("{}{}{}{}\n".format(level_space, title, title_page_space, cur))
            f.write("{}{}{}{}\n".format(level_space, title, title_page_space, page))
            #f.write("{}{}\n".format(title.strip()[:-1],page))
            #prepage = page
    return "The bookmarks have been exported to %s" % bookmark_txt_path


if __name__ == "__main__":
     pdfPath = "C:\\Users\\SWEENEY_HE\\Desktop\\软件工程导论第5版.pdf"
     pdfMark = "C:\\Users\\SWEENEY_HE\\Desktop\\软件工程导论第5版OCR.pdf.txt"
     print(extractBookmark(pdfPath, pdfMark))