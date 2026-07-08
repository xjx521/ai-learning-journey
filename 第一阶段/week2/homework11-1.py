### Day 11：文件操作

#### 题目 1：读写 txt 文件 ⭐⭐

with open("diary.txt","w",encoding='utf-8') as f:
    f.write("""
                2026-7-8
                今天学习了Python文件操作
                感觉很有趣！
                """)

with open("diary.txt","r",encoding='utf-8') as f:
    print(f.read())
    
with open("diary.txt","a",encoding='utf-8') as f:#按用途分开：写用 "w"，追加用 "a"，读用 "r"
    f.write("明天继续加油！\n")
    
with open("diary.txt","r",encoding='utf-8') as f:
    print(f.read())



