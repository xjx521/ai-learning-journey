# 基础父类：负责控制台打印信息
class Displayer:
    def display(self, message):
        # 单纯把传入的文本打印到终端
        print(message)


# Mixin混入类：提供日志写入文件的功能
class LoggerMixin:
    # 日志写入方法，默认写入 logfile.txt
    def log(self, message, filename="logfile.txt"):
        # 以追加模式打开文件，不存在则新建
        with open(filename, "a") as f:
            # 将信息写入文件
            f.write(message)

    # 重写display方法：先调用父类打印，再调用自身log写入日志
    def display(self, message):
        # super() 按照继承顺序调用上一级父类的display（即Displayer.display）
        super().display(message)
        # 调用本类log方法，把内容存进文件
        self.log(message)


# 子类：多继承，先继承LoggerMixin，再继承Displayer
class MySubClass(LoggerMixin, Displayer):
    # 重写父类LoggerMixin的log方法，修改日志文件名
    def log(self, message):
        # 调用父类LoggerMixin的log方法，指定新的日志文件
        super().log(message, filename="subclasslog.txt")


# 实例化子类对象
subclass = MySubClass()
# 调用display方法
subclass.display("This is a test.")