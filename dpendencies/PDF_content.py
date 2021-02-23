
""""添加目录方法源文件"""

import re
import string
import sys

from distutils.version import LooseVersion
from os.path import exists, splitext
from PyPDF2 import PdfFileReader, PdfFileWriter


is_python2 = LooseVersion(sys.version) < '3'


def _get_parent_bookmark(current_indent, history_indent, bookmarks):
    '''The parent of A is the nearest bookmark whose indent is smaller than A's
    '''
    assert len(history_indent) == len(bookmarks)
    if current_indent == 0:
        return None
    for i in range(len(history_indent) - 1, -1, -1):
        # len(history_indent) - 1   ===>   0
        if history_indent[i] < current_indent:
            return bookmarks[i]
    return None

def addBookmark(pdf_path, bookmark_txt_path, page_offset):
    if not exists(pdf_path):
        raise Exception("Error: No such file: {}".format(pdf_path))
    if not exists(bookmark_txt_path):
        raise Exception("Error: No such file: {}".format(bookmark_txt_path))

    with open(bookmark_txt_path, 'r',encoding='utf-8') as f:
        bookmark_lines = f.readlines()
    reader = PdfFileReader(pdf_path)
    writer = PdfFileWriter()
    writer.cloneDocumentFromReader(reader)

    maxPages = reader.getNumPages()
    bookmarks, history_indent = [], []
    # decide the level of each bookmark according to the relative indent size in each line
    #   no indent:          level 1
    #     small indent:     level 2
    #       larger indent:  level 3
    #   ...
    #排除特殊符号
    #保留字母、数字、中文、中文括号，其他自定义需要保留的可以自行添加到此处
    rule = re.compile(r"[^a-zA-Z0-9（）【】\u4e00-\u9fa5]")
    for line in bookmark_lines:
        line2 = rule.sub(' ',line)
        line2 = re.split(r'\s+', unicode(line2.strip(), 'utf-8')) if is_python2 else re.split(r'\s+', line2.strip())
        if len(line2) == 1:
            continue

        indent_size = len(line) - len(line.lstrip())
        parent = _get_parent_bookmark(indent_size, history_indent, bookmarks)
        history_indent.append(indent_size)

        title, page = ' '.join(line2[:-1]), int(line2[-1]) - 1
        if page + page_offset >= maxPages:
            raise Exception("Error: page index out of range: %d >= %d" % (page + page_offset, maxPages))
        new_bookmark = writer.addBookmark(title, page + page_offset, parent=parent)
        bookmarks.append(new_bookmark)

    out_path = splitext(pdf_path)[0] + '-new.pdf'
    with open(out_path,'wb') as f:
        writer.write(f)

    return "The bookmarks have been added to %s" % pdf_path


if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) != 4:
        print("Usage: %s [pdf] [bookmark_txt] [page_offset]" % args[0])
    pdfPath = ""
    contentPath=""
    offset=10
    print(addBookmark(pdfPath,contentPath, offset))


