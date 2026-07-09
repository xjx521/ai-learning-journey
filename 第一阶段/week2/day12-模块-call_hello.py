import day12_模块_hello

day12_模块_hello.say_hi()
day12_模块_hello.say_hello()

##from day12_模块_hello import *#*可导入所有对象 如果重名后倒入会覆盖前导入的模块 
##但是对于包来说如果没有定义__all__那么from day12_模块_hello import *将不会导入包里面任何模块
##print("x=",x)
##
##say_hello()
##print("s=",s)
##say_hi()

import day12_模块_hello as h
h.say_hi()
h.say_hello()
