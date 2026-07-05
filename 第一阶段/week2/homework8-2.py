#### 题目 2：默认参数和关键字参数 ⭐⭐

def make_coffee(size="中杯",sugar=2,milk=True):
    if milk==True:
        if sugar==0:
            print(f"{size}咖啡，不加糖，加奶")
        else:
            print(f"{size}咖啡，加{sugar}份糖，加奶")
    else:
        if sugar==0:
            print(f"{size}咖啡，不加糖，不加奶")
        else:
            print(f"{size}咖啡，加{sugar}份糖，不加奶")

make_coffee()
make_coffee("大杯")
make_coffee(sugar=0)
make_coffee("小杯",1,False)
