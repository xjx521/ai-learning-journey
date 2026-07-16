Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
def exchange(dollar,rate=6.32):
    """
    函数文档
    功能：汇率转换 美元->人民币
    -dollar 美元
    ——rate 汇率 默认值6.32
    返回值：
    -人民币
    """
    return dollar*rate

exchange(20)
126.4
help(exchange)
Help on function exchange in module __main__:

exchange(dollar, rate=6.32)
    函数文档
    功能：汇率转换 美元->人民币
    -dollar 美元
    ——rate 汇率 默认值6.32
    返回值：
    -人民币

>>> #类型注解
...     
>>> def times(s:str,n:int) -> str:#函数希望传入s为str n为int ->结果为str
...     return s*n
... 
>>> times('fishc',5)
'fishcfishcfishcfishcfishc'
>>> #只希望不阻止
>>> def times(s:str = 'fishc',n:int = 3) -> str:#函数希望传入s为str n为int ->结果为str
...     return s*n
... 
>>> times()
'fishcfishcfishc'
>>> def times(s:list[int],n:int = 3) -> list:#期待传入整数列表
...     return s*n
... 
>>> times([1,2,3])
[1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> def times(s:dict[str,int],n:int = 3) -> list:#期待传入字典，键为str  值为int
...     return list(s.keys())*n
... 
>>> times({'A':1,'B':2})
['A', 'B', 'A', 'B', 'A', 'B']
>>> times.__annotations__#查看类型注释
{'s': dict[str, int], 'n': <class 'int'>, 'return': <class 'list'>}
>>> times.__name__
'times'
>>> exchange.__doc__#查看函数文档
'\n函数文档\n功能：汇率转换 美元->人民币\n-dollar 美元\n——rate 汇率 默认值6.32\n返回值：\n-人民币\n'
