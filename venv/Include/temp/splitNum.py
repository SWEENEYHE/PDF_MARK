
#使用tab分隔中文后面紧接的数字
def split():
    lines = []
    outs = []
    #先都读进内存避免拖慢速度
    with open("C:\\Users\\SWEENEY_HE\Desktop\\new.txt","r",encoding="utf-8") as file:
        lines = file.readlines()
    #遍历
    for line in lines:
        afterLine = identyChineseAndNum(line.strip('\n'))
        outs+="".join(afterLine)+"\n"
    with open("C:\\Users\\SWEENEY_HE\Desktop\\new-new.txt","w",encoding="utf-8") as write:
        write.writelines(outs)



#识别中文与数字分隔开来,从后往前找
def identyChineseAndNum(text):
    out = []
    l = len(text)
    # 先将全部放到out中
    for i in range(0, l):
        out.append(text[i])
    #给append延长1位
    out.append(0)

    for i in range(l-1,-1,-1):
        #不是数字
        if text[i]<'0' or text[i]>'9':
            #第i+1个位置放一个tab
            out[i+1] = '\t'
            j = i+1
            #将数字往后移动到out中
            while j<l:
                out[j+1] = text[j]
                j+=1
            break

    return out


# out = identyChineseAndNum("第1章 C++的初步知识3")
# print("".join(out))
split()


