#### 题目 3：map 和 filter ⭐⭐

mapped=map(lambda x:x*3,[1,2,3,4,5])

is_positive=filter(lambda x:x if x>0 else '',[1,-2,3,-4,5,-6])

mix=map(lambda y:pow(y,2),filter(lambda x:x if x%2==0 else '',[1,2,3,4,5,6]))

print("乘以3：",list(mapped))
print("正数：",list(is_positive))
print("偶数的平方：",list(mix))
