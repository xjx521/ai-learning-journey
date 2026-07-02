#### 题目 4：字典——单词计数器 ⭐⭐⭐

text="hello world hello python world hello"
count_text={}
words=text.split()

for word in words:
    if word in count_text:
        count_text[word]+=1
    else:
        count_text[word]=1

print(count_text)
