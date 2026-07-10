#### 题目 3：collections ⭐⭐⭐

import collections 

c=collections.Counter('abracadabra')
print(c.most_common(2))#找出最常见的 2 个

scores = [("数学", 85), ("语文", 90), ("数学", 92), ("语文", 88), ("数学", 78)]
d=collections.defaultdict(list)

for subject,score in scores:
    d[subject].append(score)

print('数学：',d['数学'],'语文：',d['语文'])

