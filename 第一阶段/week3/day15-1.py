##class Turtle:#类
##属性
##    head=1
##    eyes=2
##    legs=4
##    shell=True 
##
###方法
##    def crawl(self):
##        print('慢')
##
##    def run(self):
##        print('gogogo')
##
##    def bite(self):
##        print('吃吃吃')
##
##    def sleep(self):
##        print('Zzzz...')


#没加__init__所有乌龟都共享相同属性

#__init__所有乌龟都有不同名字等属性

class Turtle:
    def __init__(self,name,age,color="绿色"):
        """构造方法：创建乌龟时自动调用"""
        self.name=name# 实例属性：每只乌龟名字不同
        self.age=age
        self.color=color # 实例属性：有默认值"绿色"
    

         # 以下是方法
    def crawl(self):
        print(f"{self.name}正在慢悠悠地爬...")

    def run(self):
        print(f"{self.name}：gogogo！")

    def bite(self):
        print(f"{self.name}咬了一口！")

    def sleep(self):
        print(f"{self.name}：Zzzz...")

t1=Turtle('小康','3')
t2=Turtle('杰尼','1','红色')

t1.crawl()
t2.run()

print(t1.age)
print(t2.color)         
        
