#### 题目 3：*args 和 **kwargs ⭐⭐⭐

def sum_all(*args):
    return sum(args)

def print_info(**kwargs):
    print(kwargs)

print(sum_all(1,2,3))
print(sum_all(10,20,30,40))

print_info(name="小明",age=20,city="广州")
