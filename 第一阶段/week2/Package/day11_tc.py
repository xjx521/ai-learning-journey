#摄氏度->华氏度
def c2f(c):
    f=c*1.8+32
    return f

#华氏度->摄氏度
def f2c(f):
    c=(f-32)/1.8
    return c

def PrintX():
    import Package
    print(Package.x)
print("day11__name__的值是：",__name__)#如果是独立模块被执行也就是自己运行是__main__，如果不是就是文件名

#测试
if __name__ == "__main__":#判断啊作为独立模块执行时运行以下

    print(f"测试，0 摄氏度={c2f(0):.2f}华氏度")
    print(f"测试，0 华氏度={f2c(0):.2f}摄氏度")
    PrintX()
