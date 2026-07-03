#### 题目 4：凯撒密码 ⭐⭐⭐

print("===凯撒密码===")

word=input("请输入要加密的文字（英文）：")
run=int(input("请输入偏移量："))

new_word = ''.join(chr((ord(i)-97+run)%26+97) for i in word)
print("加密结果：",new_word)

answer=input("要解密吗？(y/n)：")
if answer=='y':
    print("解密结果：",word)


