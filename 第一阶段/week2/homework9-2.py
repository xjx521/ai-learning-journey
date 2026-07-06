#### 题目 2：lambda 表达式 ⭐⭐

square=lambda x:pow(x,2)

is_positive=lambda x:True if x>0 else False

sort=lambda students:sorted(students,key=lambda x:x[1])

print("square(5) = ",square(5))
print("is_positive(-3) = ",is_positive(-3))
print("按成绩排序：",sort([('Alice',85),("Bob",92),("Charlie",78)]))
