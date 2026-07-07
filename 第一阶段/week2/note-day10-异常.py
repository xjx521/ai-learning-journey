Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
try:
    1/0
except ZeroDivisionError as e:
    print(e)

division by zero
try:
    1/0
except ZeroDivisionError as e:#as 可以获取原因
    print(e)

division by zero
try:
    1/0
except :
    print("出错了")

出错了
try:
    1/0
    520+"fishc"
except(ZeroDivisionError,ValueError,TypeError):
    pass


try:
    1/0
    520+"fishc"
except ZeroDivisionError:#检测到异常直接被输出不继续执行
    print("除数不为0")
except  ValueError:
    print("值不正确")
except  TypeError:
    print("类型不正确")

除数不为0
try:
    1/0
except :
    print("出错了")
else:
    print("没毛病")

出错了
try:
    1/1
except :
    print("出错了")
else:
    print("没毛病")

1.0
没毛病
try:
    1/1
except :
    print("出错了")
else:
    print("没毛病")
finally:
    print("错没错都会讲一声")

1.0
没毛病
错没错都会讲一声
try:
    f.open("fishc.txt","w")
    f.write("i love fishc")
except:
    print("出错了")
finally:
    f.close()

出错了
Traceback (most recent call last):
  File "<pyshell#37>", line 7, in <module>
    f.close()
NameError: name 'f' is not defined
try:
    f=open("fishc.txt","w")
    f.write("i love fishc")
except:
    print("出错了")
finally:
    f.close()

12
try:
    while True:
        pass
finally:
    print("good night")

good night
Traceback (most recent call last):
  File "<pyshell#45>", line 2, in <module>
    while True:
KeyboardInterrupt


#异常嵌套
try:
    try:
        520+"fishc"
    except:
        print("内部异常")
    1/0#位置在内部异常下会输出内外异常
except:
    print("外部异常")
finally:
    print("end")

内部异常
外部异常
end
try:
    1/0#检测到异常直接抛出不执行下面
    try:
        520+"fishc"
    except:
        print("内部异常")
except:
    print("外部异常")
finally:
    print("end")

外部异常
end
#raise
raise ValueError("值不正确")
Traceback (most recent call last):
  File "<pyshell#61>", line 1, in <module>
    raise ValueError("值不正确")
ValueError: 值不正确
try:
    1/0
except:
    raise ValueError("被识破了")

Traceback (most recent call last):
  File "<pyshell#67>", line 2, in <module>
    1/0
ZeroDivisionError: division by zero

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#67>", line 4, in <module>
    raise ValueError("被识破了")
ValueError: 被识破了
>>> raise ValueError("这样不行") from ZeroDivisionError
ZeroDivisionError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#68>", line 1, in <module>
    raise ValueError("这样不行") from ZeroDivisionError
ValueError: 这样不行
>>> #assert 代码调试
>>> s="fishc"
>>> assert s=="fishc"
>>> assert s!="fishc"
Traceback (most recent call last):
  File "<pyshell#72>", line 1, in <module>
    assert s!="fishc"
AssertionError
>>> #goto
>>> try:
...     while True:
...         while True:
...             for i in range(10):
...                 if i>3:
...                     raise
...                 print(i)
...             print("被跳过")
...         print("被跳过")
...     print("被跳过")
... except:
...     print("到这里来")
... 
0
1
2
3
到这里来
