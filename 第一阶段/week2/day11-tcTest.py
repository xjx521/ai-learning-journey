import Package 


print(__name__)#如果此模块单独执行是他的名称为__main__

print(f"32摄氏度等于{Package.day11_tc .c2f(32):.2f}华氏度")
print(f"99华氏度等于{Package.day11_tc .c2f(99):.2f}摄氏度")
Package.day11_tc .PrintX()
print(f"Package.x={Package.x}")

Package.x=250#修改全局变量
Package.day11_tc .PrintX()
