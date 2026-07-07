#### 题目 3：try/except/finally ⭐⭐⭐

def safe_read(filename):
    f=None# ← 先初始化为 None，保证 f 一定存在 否则f 还是不存在！照样 UnboundLocalError
    try:
        f= open(filename,'r',encoding='utf-8')
        context=f.read()
        return context
    except FileNotFoundError:
        print(f"{filename} 文件不存在")
        return None

    finally:
        if f:
            f.close()
            print("文件已关闭")

print(safe_read('homework10-1.py'))
print(safe_read('不存在.txt'))
