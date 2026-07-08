Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
f.open("fishc.txt","w")
Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    f.open("fishc.txt","w")
NameError: name 'f' is not defined
f=f.open("fishc.txt","w")
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    f=f.open("fishc.txt","w")
NameError: name 'f' is not defined
f=open("fishc.txt","w")
f.write("i love python")
13
f.writelines(["i love 111\n","i love xjx"])#传入多个字符串
f.close()
f=open("fishc.txt","r+")#即可写入也可读取
f.readable()
True
f.writeable()
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    f.writeable()
AttributeError: '_io.TextIOWrapper' object has no attribute 'writeable'. Did you mean: 'writable'?
f.writable()
True
for each in f:
    print(each)#遍历输出文件内容

i love pythoni love 111

i love xjx
f.tell()#追踪文件指针
35
f.seek(0)#修改文件指针位置
0
f.readline()
'i love pythoni love 111\n'
f.read()
'i love xjx'
f.write("i love jly")
10
f.flush()#不关闭文件写入
f.read()
''
f.seek(35)
35
f.read()
'i love jly'
f.truncate(35)
35
f.truncate(35)#截取文件
35
f.close()
f=open("fishc.txt","w")#w模式下打开会对源文件覆盖截取
#pathlib
from pathlib import Path#从path包中单独导入pathlib
Path.cwd()#查看当前路径
WindowsPath('C:/Users/xjxx/OneDrive/文档')
p=Path('C:/Users/xjxx/OneDrive/文档')#生成路径对象
q=p/"fishc.txt"#把fishc添加到p路径
q
WindowsPath('C:/Users/xjxx/OneDrive/文档/fishc.txt')
p.is_dir()#是否为文件夹
True
q.is_file()#是否为文件
True
Path("C/12315262").exists()#检测路径是否存在
False
q.name#获取路径最后部分
'fishc.txt'
q.stem#获取文件名
'fishc'
q.suffix#获取文件后缀
'.txt'
p.parent#父级目录
WindowsPath('C:/Users/xjxx/OneDrive')
p.parents#父级目录构成的不可变序列
<WindowsPath.parents>
ps=p.parents
for each in ps:
    print(each)

C:\Users\xjxx\OneDrive
C:\Users\xjxx
C:\Users
C:\
ps[0]
WindowsPath('C:/Users/xjxx/OneDrive')
ps[1]
WindowsPath('C:/Users/xjxx')
p.parts#将路径拆分成元组
('C:\\', 'Users', 'xjxx', 'OneDrive', '文档')
p.stat()#查看文件信息
os.stat_result(st_mode=16749, st_ino=562949953462428, st_dev=65018073500716386, st_nlink=1, st_uid=0, st_gid=0, st_size=8192, st_atime=1783497876, st_mtime=1783497874, st_ctime=1709470338)
p.stat().st_size#查看文件
8192
#相对路径/绝对路径
Path("./doc")#当前doc的相对路径
WindowsPath('doc')
Path("../fishc")#当前fish的相对路径的上一个路径
WindowsPath('../fishc')
Path("../fishc").resolve()#转换成绝对路径
WindowsPath('C:/Users/xjxx/OneDrive/fishc')
p.iterdir()#获取子文件夹和子文件
<map object at 0x0000029770285600>
a=p.iterdir()
for each in a:
    print(each)

C:\Users\xjxx\OneDrive\文档\CD Projekt Red
C:\Users\xjxx\OneDrive\文档\CPY_SAVES
C:\Users\xjxx\OneDrive\文档\desktop.ini
C:\Users\xjxx\OneDrive\文档\DyingLight
C:\Users\xjxx\OneDrive\文档\fishc.txt
C:\Users\xjxx\OneDrive\文档\IISExpress
C:\Users\xjxx\OneDrive\文档\KingsoftData
C:\Users\xjxx\OneDrive\文档\KOOK
C:\Users\xjxx\OneDrive\文档\MuMu共享文件夹
C:\Users\xjxx\OneDrive\文档\My Games
C:\Users\xjxx\OneDrive\文档\My Web Sites
C:\Users\xjxx\OneDrive\文档\Navicat
C:\Users\xjxx\OneDrive\文档\OneNote Notebooks
C:\Users\xjxx\OneDrive\文档\Rise of the Tomb Raider
C:\Users\xjxx\OneDrive\文档\Rockstar Games
C:\Users\xjxx\OneDrive\文档\Sunlogin Files
C:\Users\xjxx\OneDrive\文档\The Witcher 3
C:\Users\xjxx\OneDrive\文档\Visual Studio 2022
C:\Users\xjxx\OneDrive\文档\WeChat Files
C:\Users\xjxx\OneDrive\文档\Winstep.lnk
C:\Users\xjxx\OneDrive\文档\WPSDrive
C:\Users\xjxx\OneDrive\文档\今天.docx
C:\Users\xjxx\OneDrive\文档\自定义 Office 模板
[x for x in p.iterdir() if x.is_file()]#收集文件
[WindowsPath('C:/Users/xjxx/OneDrive/文档/desktop.ini'), WindowsPath('C:/Users/xjxx/OneDrive/文档/fishc.txt'), WindowsPath('C:/Users/xjxx/OneDrive/文档/Winstep.lnk'), WindowsPath('C:/Users/xjxx/OneDrive/文档/今天.docx')]
n=p/"fishc"
n.mkdir()#创建文件夹
n=p/"fishc/a/b/c"
n.mkdir(parents=True,exist_ok=True)#创建文件夹,parents避免有不存在父类报错，exist_ok,避免文件存在时候报错
n=n/"fishc.txt"
n
WindowsPath('C:/Users/xjxx/OneDrive/文档/fishc/a/b/c/fishc.txt')
f=n.open("w")
f.write("i love fishc")
12
f.close()
n.rename("newfishc.txt")#改名
WindowsPath('newfishc.txt')
m=Path("newfishc.txt")
m.replace(n)#替换
WindowsPath('C:/Users/xjxx/OneDrive/文档/fishc/a/b/c/fishc.txt')
n.parent.rmdir()#删除文件夹
Traceback (most recent call last):
  File "<pyshell#71>", line 1, in <module>
    n.parent.rmdir()#删除文件夹
  File "C:\Users\xjxx\AppData\Local\Python\pythoncore-3.13-64\Lib\pathlib\_local.py", line 755, in rmdir
    os.rmdir(self)
OSError: [WinError 145] 目录不是空的。: 'C:\\Users\\xjxx\\OneDrive\\文档\\fishc\\a\\b\\c'
n.unlink()#删除文件
n.parent.rmdir()#删除文件夹
p=Path(".")
p,glob("*.txt")#查找
Traceback (most recent call last):
  File "<pyshell#75>", line 1, in <module>
    p,glob("*.txt")#查找
NameError: name 'glob' is not defined. Did you forget to import 'glob'?
p.glob("*.txt")#查找
<map object at 0x0000029770285CC0>
list(p.glob("*.txt"))
[WindowsPath('fishc.txt')]
list(p.glob("*/.txt"))
[]
>>> list(p.glob("*/.txt"))#查找当前目录下一级
[]
>>> list(p.glob("*/*.txt"))#查找当前目录下一级
[WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_2024-10-24_23.18.40.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_2024-10-24_23.23.09.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_frametimes_2024-10-24_23.18.40.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_frametimes_2024-10-24_23.23.09.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_2024-10-24_23.17.44.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_2024-10-24_23.22.38.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_frametimes_2024-10-24_23.17.44.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_frametimes_2024-10-24_23.22.38.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-24_23.17.02.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-24_23.22.12.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-28_18.37.29.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-24_23.17.02.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-24_23.22.12.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-28_18.37.29.txt')]
>>> list(p.glob("**/*.txt"))#查找当前目录所有.txt
[WindowsPath('fishc.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_2024-10-24_23.18.40.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_2024-10-24_23.23.09.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_frametimes_2024-10-24_23.18.40.txt'), WindowsPath('Rise of the Tomb Raider/GeothermalValley_极光_frametimes_2024-10-24_23.23.09.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_2024-10-24_23.17.44.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_2024-10-24_23.22.38.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_frametimes_2024-10-24_23.17.44.txt'), WindowsPath('Rise of the Tomb Raider/ProphetsTomb_极光_frametimes_2024-10-24_23.22.38.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-24_23.17.02.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-24_23.22.12.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_2024-10-28_18.37.29.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-24_23.17.02.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-24_23.22.12.txt'), WindowsPath('Rise of the Tomb Raider/SpineOfTheMountain_极光_frametimes_2024-10-28_18.37.29.txt'), WindowsPath('Rockstar Games/Red Dead Redemption 2/Benchmarks/Benchmark-24-03-04-20-34-51.txt')]
#pickle
#可以存于所有类型load/dump
#with open("1.txt","w") as f:
      #f.wirte("111")
