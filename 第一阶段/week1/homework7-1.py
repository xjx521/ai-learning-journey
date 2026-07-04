### Day 7：综合练习（复习日）

#### 题目 1：FizzBuzz ⭐⭐

for i in range(1,101):
    if i%3==0 and i%5!=0:
        print("Fizz")
    elif i%5==0 and i%3!=0:
        print("Buzz")
    elif i%3==0 and i%5==0:
        print("FizzBuzz")
    else:
        print(i)
