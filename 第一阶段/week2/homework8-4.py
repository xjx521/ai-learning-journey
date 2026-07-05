#### 题目 4：返回多个值 ⭐⭐

def analyze_numbers(numbers):
    return {'max':max(numbers),'min':min(numbers),'avg':sum(numbers)/len(numbers),'sum':sum(numbers)}

print(analyze_numbers([3,7,1,9,4]))
