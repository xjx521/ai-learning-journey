"""
Day 25 练习题：Python 异步编程基础
================================

💡 提示：今天重点理解"同步 vs 异步"的执行顺序差异。
运行代码时注意观察输出顺序和耗时。
"""

import asyncio
import time


# ============================================================
# 【练习 1】理解执行顺序（先预测，再运行验证）
# ============================================================
"""
阅读以下代码，先预测输出顺序和总耗时，再运行验证。

问题 1.1：输出的顺序是什么？
  你的预测：_____________

问题 1.2：总耗时大约是多少秒？
  你的预测：_____________
"""

async def task_a():
    print("A: 开始")
    await asyncio.sleep(1)
    print("A: 完成")

async def task_b():
    print("B: 开始")
    await asyncio.sleep(2)
    print("B: 完成")

async def task_c():
    print("C: 开始")
    await asyncio.sleep(0.5)
    print("C: 完成")

async def exercise_1():
    print("=" * 50)
    print("【练习 1】理解执行顺序")
    print("=" * 50)
    start = time.time()

    # 💡 提示：gather 会同时启动所有协程
    await asyncio.gather(task_a(), task_b(), task_c())

    elapsed = time.time() - start
    print(f"\n总耗时：{elapsed:.1f} 秒")


# ==================== 参考答案 ====================
# 1.1 输出顺序：A: 开始 → B: 开始 → C: 开始 → C: 完成 → A: 完成 → B: 完成
#     （三个同时开始，C 最先完成(0.5s)，然后 A(1s)，最后 B(2s)）
# 1.2 总耗时：约 2.0 秒（取决于最慢的 task_b）


# ============================================================
# 【练习 2】同步 vs 异步 耗时对比
# ============================================================
"""
这个练习对比同步和异步的耗时差异。
你需要补全异步部分的代码。
"""

def sync_fetch(name, delay):
    """模拟同步网络请求"""
    time.sleep(delay)
    return f"{name} 的数据"

async def async_fetch(name, delay):
    """模拟异步网络请求"""
    # TODO：用 asyncio.sleep 替代 time.sleep
    # 💡 提示：await asyncio.sleep(delay)
    await asyncio.sleep(delay)
    return f"{name} 的数据"

def exercise_2():
    print("\n" + "=" * 50)
    print("【练习 2】同步 vs 异步 耗时对比")
    print("=" * 50)

    # --- 同步版本 ---
    print("\n📌 同步执行：")
    start = time.time()
    results_sync = []
    for name in ["用户", "订单", "商品"]:
        result = sync_fetch(name, 1)
        results_sync.append(result)
        print(f"  获取到 {result}")
    sync_time = time.time() - start
    print(f"  同步总耗时：{sync_time:.1f} 秒")

    # --- 异步版本 ---
    async def run_async():
        print("\n📌 异步执行：")
        start = time.time()

        # TODO：用 asyncio.gather 并发执行三个 async_fetch
        # 💡 提示：
        #   tasks = [async_fetch("用户", 1), async_fetch("订单", 1), async_fetch("商品", 1)]
        #   results = await asyncio.gather(*tasks)
        tasks = [async_fetch("用户", 1), async_fetch("订单", 1), async_fetch("商品", 1)]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(f"  获取到 {result}")
        async_time = time.time() - start
        print(f"  异步总耗时：{async_time:.1f} 秒")
        return sync_time, async_time

    sync_time, async_time = asyncio.run(run_async())

    print(f"\n💡 同步耗时 {sync_time:.1f}s vs 异步耗时 {async_time:.1f}s")
    print(f"   异步快了约 {sync_time / async_time:.1f} 倍！")


# ==================== 参考答案 ====================
# 已在代码中直接展示


# ============================================================
# 【练习 3】实现异步爬虫雏形
# ============================================================
"""
模拟一个"爬虫"场景：需要从 5 个网站获取数据，每个网站响应时间不同。
"""

async def fetch_website(name, delay):
    """模拟请求一个网站"""
    print(f"  ⏳ 开始获取 {name}（需要 {delay} 秒）...")
    await asyncio.sleep(delay)
    print(f"  ✅ {name} 获取完成！")
    return {"site": name, "data": f"来自 {name} 的数据", "time": delay}

async def exercise_3():
    print("\n" + "=" * 50)
    print("【练习 3】异步爬虫模拟")
    print("=" * 50)

    websites = [
        ("百度", 0.5),
        ("GitHub", 2.0),
        ("知乎", 1.0),
        ("B站", 1.5),
        ("豆瓣", 0.8),
    ]

    # TODO 1：用 asyncio.gather 并发获取所有网站
    # 💡 提示：先用列表推导式创建任务列表，再传给 gather
    start = time.time()

    tasks = [fetch_website(name, delay) for name, delay in websites]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"\n📊 结果汇总：")
    for r in results:
        print(f"  {r['site']}：{r['data']}")
    print(f"\n⏱️  总耗时：{elapsed:.1f} 秒")
    print(f"   如果同步执行需要：{sum(d for _, d in websites):.1f} 秒")
    print(f"   异步节省了：{sum(d for _, d in websites) - elapsed:.1f} 秒")

    # TODO 2：只获取最快的前 3 个结果
    # 💡 提示：用 asyncio.as_completed() 或在 gather 后按 time 排序
    print("\n📌 获取最快的前 3 个：")
    sorted_results = sorted(results, key=lambda x: x["time"])
    for r in sorted_results[:3]:
        print(f"  {r['site']}（{r['time']} 秒）")


# ==================== 参考答案 ====================
# 已在代码中直接展示


# ============================================================
# 【练习 4】async/await 常见错误（找茬）
# ============================================================
"""
以下代码有错误，请找出并修正。

代码 1：
```python
async def greet(name):
    return f"Hello, {name}"

result = greet("World")
print(result)
```
问题：____________________________________
修正：____________________________________

代码 2：
```python
def fetch_data():
    data = await some_api_call()
    return data
```
问题：____________________________________
修正：____________________________________

代码 3：
```python
async def slow_task():
    time.sleep(5)  # 阻塞调用
    return "done"
```
问题：____________________________________
修正：____________________________________
"""

# ==================== 参考答案 ====================
def check_exercise_4():
    print("=" * 50)
    print("【练习 4 参考答案】找茬")
    print("=" * 50)
    print("""
代码 1：
  问题：调用协程函数得到的是协程对象，不是结果。且没有用 asyncio.run()
  修正：result = asyncio.run(greet("World"))

代码 2：
  问题：await 只能在 async def 内部使用，普通 def 中不能用 await
  修正：将 def fetch_data() 改为 async def fetch_data()

代码 3：
  问题：在 async 函数中使用 time.sleep() 会阻塞整个事件循环
  修正：将 time.sleep(5) 改为 await asyncio.sleep(5)
    """)


# ============================================================
# 【练习 5】动手：写一个异步计时器
# ============================================================
async def countdown(name, seconds):
    """
    异步倒计时器

    TODO：
    1. 从 seconds 倒数到 1
    2. 每秒打印一次 "[name] 剩余 X 秒"
    3. 最后打印 "[name] 时间到！"
    4. 使用 await asyncio.sleep(1) 而不是 time.sleep(1)
    """
    # 在这里写你的代码
    pass

async def exercise_5():
    print("\n" + "=" * 50)
    print("【练习 5】异步倒计时器")
    print("=" * 50)

    # TODO：同时启动两个倒计时器
    # 一个 "Timer A" 3 秒，一个 "Timer B" 5 秒
    # 💡 提示：用 asyncio.gather
    #
    # 你的代码写在这里：

    await asyncio.gather(
        countdown("Timer A", 3),
        countdown("Timer B", 5),
    )


# ==================== 参考答案 ====================
async def countdown_answer(name, seconds):
    for i in range(seconds, 0, -1):
        print(f"  [{name}] 剩余 {i} 秒")
        await asyncio.sleep(1)
    print(f"  [{name}] 🎉 时间到！")


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 70 - 爬楼梯（Easy）
#    链接：https://leetcode.cn/problems/climbing-stairs/
#    关联：今天学了并发，爬楼梯可以理解为"并行选择"
#    思路提示：动态规划，dp[i] = dp[i-1] + dp[i-2]
#
# 2. LeetCode 21 - 合并两个有序链表（Easy）
#    链接：https://leetcode.cn/problems/merge-two-sorted-lists/
#    思路提示：用虚拟头节点，依次比较两个链表的当前节点
#
# 💡 两道都是面试高频题
# ============================================================


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("\n" + "🚀 " * 15)
    print("  Day 25 异步编程基础 - 练习开始")
    print("🚀 " * 15 + "\n")

    async def run_all():
        await exercise_1()
        exercise_2()
        await exercise_3()
        check_exercise_4()

        # 练习 5：先运行你的版本，再运行参考答案
        print("\n--- 你的版本 ---")
        await exercise_5()
        print("\n--- 参考答案 ---")
        await asyncio.gather(
            countdown_answer("Timer A", 3),
            countdown_answer("Timer B", 5),
        )

    asyncio.run(run_all())

    print("\n" + "=" * 50)
    print("🎉 所有练习运行完毕！")
    print("📌 别忘了做今天的 LeetCode 推荐题！")
    print("=" * 50)
