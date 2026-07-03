Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
x=input("输入数字：")
输入数字：12321
"是回文数"if x==x[::-1] else "不是回文数"
'是回文数'
x=input("输入数字：")
输入数字：123
"是回文数"if x==x[::-1] else "不是回文数"
'不是回文数'
#大小写转换
x="I love Fish"
x.capitalize()
'I love fish'
x.casefold()
'i love fish'
x.title()
'I Love Fish'
x.swapcase()#大小写反转
'i LOVE fISH'
x.upper()
'I LOVE FISH'
x.lower()
'i love fish'
x.capitalize()#首字母大写
'I love fish'
#对齐
x="有内鬼，终止交易！"
x.center(5)
'有内鬼，终止交易！'
x.center(15)#居中对齐，width变量要大于字符串
'   有内鬼，终止交易！   '
x.ljust(15)
'有内鬼，终止交易！      '
x.rjust(15)#右
'      有内鬼，终止交易！'
"520".zfill(5)#0左填充
'00520'
x.center(15，"牛")#居中对齐，width变量要大于字符串
SyntaxError: invalid character '，' (U+FF0C)
x.center(15,"牛")#居中对齐，width变量要大于字符串
'牛牛牛有内鬼，终止交易！牛牛牛'
#查找
x="上海自来水来自海上"
x.count("海",0,5)
1
x.count("海")
2
x.find("海")
1
x.rfind("海",-1,-5)#右往左
-1
x.index("海")
1
x.index(6)
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    x.index(6)
TypeError: index() argument 1 must be str, not int
x.rindex("海")#右往左同样找索引值但是会抛出异常
7
#替换
"我是xjx".replace("xjx","jly")
'我是jly'
code="""
    tab
   space"""
n_code=code.expandtabs(3)#tab换空格
print(n_code)

    tab
   space
table=str.maketrans("ABCDEFG","1234567")
table
{65: 49, 66: 50, 67: 51, 68: 52, 69: 53, 70: 54, 71: 55}
"I love FishC".translate(table)
'I love 6ish3'
"I love FishC".translate(str.maketrans("ABCDEFG","1234567","love") )#表格转换,第三个参数指定字符串忽略
'I  6ish3'
#判断
x="我爱Python"
x.startswith("我")#判断是否在起始位置
True
x.endtswith("py")#判断是否在结束位置
Traceback (most recent call last):
  File "<pyshell#43>", line 1, in <module>
    x.endtswith("py")#判断是否在结束位置
AttributeError: 'str' object has no attribute 'endtswith'. Did you mean: 'endswith'?
x.endswith("py")#判断是否在结束位置
False
x.endswith("py"，0，4)#判断是否在结束位置
SyntaxError: invalid character '，' (U+FF0C)
x.endswith("py",0,4)#判断是否在结束位置
False
x.endswith("Py",0,4)#判断是否在结束位置
True
x="她爱pyhon"
if x.startswith(("你","我","她")):
    print("good")#元组输入多个

good
x="I love Python"
x.istitle()#是否首字母为大写其他都是小写
False
x.isupper()#大写
False
x.upper().isupper()
True
s.islower()
Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    s.islower()
NameError: name 's' is not defined
x.islower()
False
x.isalpha()#是否只有字母
False
"ilove".isalpha()
True
"    \n".isspace()#空白
True
"\n".isprintable#可打印
<built-in method isprintable of str object at 0x00007FFE48C27F90>
"\n".isprintable()#可打印
False
x="12345"
x.isdecimal()
True
x.isdigit()
True
x.isnumeric()#范围最大
True
x.isalnum()#判断数字空白字母等都可
True
x.isalnum()#判断数字字母等都可
True
"i am good".isidentifier()
False
"i_am_good".isidentifier()#合法标识符
True
import keyword
keyword.iskeyword("if")#判断保留标识符
True
keyword.iskeyword("py")#判断保留标识符
False
#截取
"      左侧不要留白".lstrip()
'左侧不要留白'
"右侧不要留白       ".rstrip()
'右侧不要留白'
"     左右侧不要留白       ".strip()
'左右侧不要留白'
"www.91short.com".strip("w.com")
'91short'
"www.91short.com".lstrip("w.com")
'91short.com'
"www.91short.com".rstrip("w.com")
'www.91short'
"www.91short.com".removeprefix("www.")#指定前缀，是字符串，上面的是字符
'91short.com'
"www.91short.com".removesuffix(".com")#指定后缀，是字符串
'www.91short'
#拆分&切割
"www.91short.com".partiton(".")#左到右切割
Traceback (most recent call last):
  File "<pyshell#84>", line 1, in <module>
    "www.91short.com".partiton(".")#左到右切割
AttributeError: 'str' object has no attribute 'partiton'. Did you mean: 'partition'?
"www.91short.com".partition(".")#左到右切割
('www', '.', '91short.com')
"www.91short.com".rpartition(".")#右到左切割
('www.91short', '.', 'com')
"aaa，bbb，ccc".split("，")
['aaa', 'bbb', 'ccc']
"aaa bbb ccc".split()#默认空格
['aaa', 'bbb', 'ccc']
"aaa bbb ccc".split(,1)#决定分割几次
SyntaxError: invalid syntax
"aaa bbb ccc".split(" ",1)#决定分割几次
['aaa', 'bbb ccc']
"aaa bbb ccc".rsplit(" ",1)
['aaa bbb', 'ccc']
"aaa bbb ccc".splitlines()#按行划分
['aaa bbb ccc']
"aaa\rbbb\nccc".splitlines()#按行划分
['aaa', 'bbb', 'ccc']
"aaa\rbbb\nccc".splitlines(True)#按行划分,True代表保留换行符
['aaa\r', 'bbb\n', 'ccc']
".".join(["www","91short","com"])#拼接，.作为里面分割符
'www.91short.com'
#格式化
"{1}爱{0}".format("我","python")
'python爱我'
"{:^10}".format(250)#width=10获得宽度，^居中
'   250    '
"{0:>10}{1:<10}".format(520,250)#width=10获得宽度，<左对齐，>右对齐
'       520250       '
"{:010}".format(-520)
'-000000520'
"{0:%>10}{1:%<10}".format(520,250)#width=10获得宽度，<左对齐，>右对齐
'%%%%%%%520250%%%%%%%'
"{:+}{:-}".format(520,-250)
'+520-250'
"{:,}".fotmat(1234)
Traceback (most recent call last):
  File "<pyshell#103>", line 1, in <module>
    "{:,}".fotmat(1234)
AttributeError: 'str' object has no attribute 'fotmat'. Did you mean: 'format'?
"{:,}".format(1234)#,_等可做千分符，位数不足不显示
'1,234'
"{:,}".format(123456789)#,_等可做千分符，位数不足不显示
'123,456,789'
"{:.2f}".format(3.1415)#小数点后保留两位
'3.14'
"{:.2g}".format(3.1415)#小数点前后一共保留两位
'3.1'
"{:.6}".format("i love python")#截取6个单位的字符串
'i love'
"{:b}".format(80)#二进制
'1010000'
"{:c}".format(80)#unicode
'P'
>>> "{:d}".format(80)#十进制
'80'
>>> "{:#o}".format(80)#十六进制，#提示符
'0o120'
>>> "{:#o}".format(80)#八进制，#提示符
'0o120'
>>> "{:#x}".format(80)#十六进制，#提示符
'0x50'
>>> "{:e}".format(3.1415)#科学计数法
'3.141500e+00'
>>> "{:g}".format(3.1415)#定点表示法
'3.1415'
>>> "{:f}".format(3.1415)#定点表示法,g:小数科学计数，大数定点表示
'3.141500'
>>> "{:%}".format(0.98)#百分数
'98.000000%'
>>> "{:.2%}".format(0.98)#百分数
'98.00%'
>>> fill="+"
>>> align="^"
>>> width=10
>>> prec=3
>>> ty='g'
>>> "f{3.1415:{fill}{width}.{prec}{ty}}"
'f{3.1415:{fill}{width}.{prec}{ty}}'
>>> f"{3.1415:{fill}{width}.{prec}{ty}}"
'     +3.14'
>>> fill="+"
>>> align="^"
>>> f"{3.1415:{fill}{width}.{prec}{ty}}"
'     +3.14'
>>> align='^'
>>> fill='+'
>>> f"{3.1415:{fill}{width}.{prec}{ty}}"
'     +3.14'
>>> f"{3.1415:{fill}{width}.{prec}{ty}}"
'     +3.14'
>>> f"{3.1415:{fill}{align}{width}.{prec}{ty}}"
'+++3.14+++'
