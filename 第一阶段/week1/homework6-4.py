#### 题目 4：凯撒密码 ⭐⭐⭐

print("===凯撒密码===")

word = input("请输入要加密的文字（英文）：")
run = int(input("请输入偏移量："))

# 加密：逐个字符处理，大小写分别用不同基准值
new_word = ''.join(
    chr((ord(i) - 97 + run) % 26 + 97) if i.islower() else   # 小写：基准 a=97
    chr((ord(i) - 65 + run) % 26 + 65) if i.isupper() else   # 大写：基准 A=65
    i                                                          # 非字母：保留原样
    for i in word
)
print("加密结果：", new_word)

answer = input("要解密吗？(y/n)：")
if answer == 'y':
    # 解密：用负偏移量反向计算
    decrypt_word = ''.join(
        chr((ord(i) - 97 - run) % 26 + 97) if i.islower() else
        chr((ord(i) - 65 - run) % 26 + 65) if i.isupper() else
        i
        for i in new_word
    )
    print("解密结果：", decrypt_word)