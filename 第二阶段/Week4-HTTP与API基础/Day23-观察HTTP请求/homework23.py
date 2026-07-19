"""
Day 23 练习题：观察真实 HTTP 请求 + 工具使用
==========================================

今天的练习和之前不同：大部分是"实验任务"而非编程题。
你需要用浏览器 F12、curl、Postman/Apifox 来完成。

⚠️ 需要安装 requests 库：pip install requests
"""

import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import json


# ============================================================
# 【练习 1】F12 观察任务（浏览器操作，无需写代码）
# ============================================================
"""
请按以下步骤操作，并将观察到的答案写在注释中。

任务 1：观察 B 站搜索 API
--------------------------
1. 打开 https://search.bilibili.com
2. F12 → Network → 点击 "Fetch/XHR" 过滤
3. 在搜索框输入 "FastAPI"（不要按回车）
4. 观察出现的请求：

   问题 1.1：请求的 URL 是什么？
   你的答案：_____________

   问题 1.2：请求方法是什么？（GET 还是 POST？）
   你的答案：_____________

   问题 1.3：在请求参数中找到你的搜索关键词了吗？参数名叫什么？
   你的答案：_____________

   问题 1.4：响应体是什么格式？（JSON / HTML / 纯文本？）
   你的答案：_____________

任务 2：观察请求头
--------------------------
1. 打开 https://httpbin.org/headers
2. F12 → Network → 刷新页面
3. 点击第一个请求（httpbin.org/headers）
4. 查看 Headers 标签：

   问题 2.1：你的浏览器 User-Agent 是什么？（复制前 50 个字符）
   你的答案：_____________

   问题 2.2：Accept 请求头的值是什么？
   你的答案：_____________

   问题 2.3：响应体的 Content-Type 是什么？
   你的答案：_____________

任务 3：观察 Cookie
--------------------------
1. 打开 https://github.com（先不要登录）
2. F12 → Network → 刷新页面 → 点击第一个请求
3. 查看 Request Headers 中有没有 Cookie？

   问题 3.1：未登录时，请求头中有 Cookie 吗？
   你的答案：_____________

4. 如果你已有 GitHub 账号，登录后再观察一次：

   问题 3.2：登录后，请求头中多了哪些 Cookie？（写出一两个名字即可）
   你的答案：_____________
"""

# ==================== 参考答案 ====================
def check_exercise_1():
    print("=" * 50)
    print("【练习 1 参考答案】F12 观察任务")
    print("=" * 50)
    print("""
任务 1（B 站搜索）：
  1.1 URL 类似：https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&keyword=FastAPI
  1.2 方法：GET
  1.3 参数名：keyword
  1.4 响应格式：JSON

任务 2（请求头）：
  2.1 User-Agent 类似：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
  2.2 Accept 通常包含：text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
  2.3 Content-Type：application/json

任务 3（Cookie）：
  3.1 未登录时也有 Cookie（如 _device_id, buvid3 等追踪标识）
  3.2 登录后会多出登录相关 Cookie（如 SESSDATA, bili_jct 等）
  💡 注意：实际观察到的 Cookie 名称可能不同
    """)


# ============================================================
# 【练习 2】用 Python 搭建一个微型 HTTP 服务器
# ============================================================
"""
这个练习帮你理解"服务器"到底是什么。
运行后，你的电脑就变成了一个 HTTP 服务器！
"""

class SimpleHandler(BaseHTTPRequestHandler):
    """
    这是一个最简单的 HTTP 请求处理器。
    它定义了：当有人来访问时，服务器该怎么回复。
    """

    def do_GET(self):
        """处理 GET 请求"""
        # 1. 设置响应状态码
        self.send_response(200)

        # 2. 设置响应头
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # 3. 根据路径返回不同内容
        if self.path == "/":
            html = "<h1>欢迎来到我的第一个服务器！🎉</h1><p>这是首页。</p>"
        elif self.path == "/about":
            html = "<h1>关于页面</h1><p>这是我 Day 23 的练习作品。</p>"
        elif self.path.startswith("/hello/"):
            # 从路径中提取名字：/hello/张三 → 张三
            name = self.path.replace("/hello/", "")
            html = f"<h1>你好，{name}！</h1>"
        else:
            self.send_response(404)
            self.end_headers()
            html = "<h1>404 - 页面不存在</h1>"
            # 注意：这里有个 bug！404 时 send_response 被调用了两次
            # 你能修复它吗？

        # 4. 写入响应体（必须是 bytes）
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """处理 POST 请求"""
        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # 尝试解析 JSON
        try:
            data = json.loads(body)
            response = {"status": "success", "received": data, "message": "服务器收到了你的数据！"}
            status = 200
        except json.JSONDecodeError:
            response = {"status": "error", "message": "请发送有效的 JSON 格式"}
            status = 400

        # 返回响应
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"  [服务器日志] {args[0]}")


def exercise_2_start_server():
    """
    启动本地 HTTP 服务器

    TODO：
    1. 运行本文件，服务器会在 http://localhost:8888 启动
    2. 打开浏览器访问以下地址：
       - http://localhost:8888/
       - http://localhost:8888/about
       - http://localhost:8888/hello/你的名字
       - http://localhost:8888/notfound （应该返回 404）
    3. 用 Postman 或 curl 发送 POST 请求到 http://localhost:8888
       Body 设为 JSON: {"name": "测试", "action": "hello"}
    4. 观察终端里的服务器日志

    按 Ctrl+C 停止服务器。
    """
    print("=" * 50)
    print("【练习 2】启动本地 HTTP 服务器")
    print("=" * 50)
    print("服务器地址：http://localhost:8888")
    print("请在浏览器中访问以下 URL：")
    print("  1. http://localhost:8888/")
    print("  2. http://localhost:8888/about")
    print("  3. http://localhost:8888/hello/你的名字")
    print("  4. http://localhost:8888/notfound")
    print("\n用 curl 或 Postman 发送 POST 请求：")
    print('  curl -X POST http://localhost:8888 -H "Content-Type: application/json" -d \'{"name":"test"}\'')
    print("\n按 Ctrl+C 停止服务器\n")
    print("-" * 50)

    server = HTTPServer(("localhost", 8888), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止 ✅")
        server.server_close()


# ==================== 参考答案 ====================
# 练习 2 中的 404 bug 修复：
# 问题：self.send_response(404) 之后没有 return，代码继续执行
#      到 self.send_response(200)（在 else 外面没有，但在 self.wfile.write 时
#      已经发了 404 的状态码，不过 html 变量被正确赋值为 404 页面）
# 实际行为：这段代码其实可以正常工作，因为 404 时 html 变量被正确赋值，
#           send_response(404) 先被调用，后面的 self.wfile.write 会用正确的状态码。
# 改进建议：用 return 提前退出更清晰
#
# 修复版本：
#     else:
#         self.send_response(404)
#         self.send_header("Content-Type", "text/html; charset=utf-8")
#         self.end_headers()
#         self.wfile.write(b"<h1>404 - 页面不存在</h1>")
#         return  # ← 加上 return 提前退出


# ============================================================
# 【练习 3】用 requests 模拟浏览器行为
# ============================================================
def exercise_3_requests_experiments():
    """
    用 requests 库完成以下实验，每个实验后回答一个问题。
    """
    print("=" * 50)
    print("【练习 3】requests 实验")
    print("=" * 50)

    # --- 实验 1：自定义 User-Agent ---
    # 💡 提示：很多网站通过 User-Agent 判断你是不是浏览器
    # 如果不设置，requests 的 UA 是 "python-requests/x.x.x"，会被一些网站拒绝
    print("\n📌 实验 1：伪装成浏览器")
    url = "https://httpbin.org/user-agent"

    # TODO：发送 GET 请求，把 User-Agent 伪装成 Chrome 浏览器
    # 参考答案在文件底部
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        print(f"  服务器看到的 User-Agent：{data.get('user-agent')}")

        # 对比：不设置 UA
        response2 = requests.get(url, timeout=10)
        data2 = response2.json()
        print(f"  默认的 User-Agent：{data2.get('user-agent')}")
        print("  💡 这就是为什么有时候用 requests 会被网站'拒绝'！")
    except Exception as e:
        print(f"  ❌ 请求失败：{e}")

    # --- 实验 2：Session 自动管理 Cookie ---
    # 💡 提示：requests.Session() 会像浏览器一样自动保存和发送 Cookie
    print("\n📌 实验 2：Session 管理 Cookie")

    session = requests.Session()

    try:
        # 第一步：访问设置 Cookie 的接口
        session.get("https://httpbin.org/cookies/set/my_cookie/hello123", timeout=10)

        # 第二步：验证 Cookie 是否被自动带上
        response = session.get("https://httpbin.org/cookies", timeout=10)
        print(f"  Cookie 数据：{response.json().get('cookies')}")
        print("  💡 Session 自动保存了 set-cookie，并在后续请求中带上！")
        print("  这就是登录状态的实现原理。")
    except Exception as e:
        print(f"  ❌ 请求失败：{e}")

    # --- 实验 3：超时设置 ---
    print("\n📌 实验 3：超时控制")

    try:
        # httpbin.org/delay/5 会延迟 5 秒响应
        print("  请求一个延迟 5 秒的接口，超时设为 2 秒...")
        response = requests.get("https://httpbin.org/delay/5", timeout=2)
        print("  这行不会被执行到")
    except requests.exceptions.Timeout:
        print("  ✅ 触发了超时异常！实际开发中要给用户友好的超时提示。")
    except Exception as e:
        print(f"  其他异常：{e}")

    print()


# ==================== 参考答案 ====================
# 实验 1 已在代码中直接展示
# 实验 2 已在代码中直接展示
# 实验 3 已在代码中直接展示


# ============================================================
# 【练习 4】curl 命令行练习（在终端中完成）
# ============================================================
"""
请打开终端（PowerShell / Git Bash / cmd），依次执行以下命令，
并观察输出结果。把看到的答案写在注释里。

命令 1：基本 GET 请求
    curl https://httpbin.org/get

    问题：响应中 "origin" 字段的值是什么？
    你的答案：_____________（这是你的公网 IP 地址）

命令 2：带参数的 GET
    curl "https://httpbin.org/get?name=test&course=http"

    问题：在响应的 "args" 中看到了什么？
    你的答案：_____________

命令 3：发送 POST 请求
    curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d "{\"message\":\"hello\"}"

    ⚠️ Windows cmd 中引号处理不同，建议用 Git Bash 或 PowerShell
    PowerShell 版本：
    curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{\"message\":\"hello\"}'

    问题：响应中 "data" 字段的值是什么？
    你的答案：_____________

命令 4：查看完整 HTTP 交互
    curl -v https://httpbin.org/get

    问题：以 > 开头的行是什么？以 < 开头的行是什么？
    你的答案：_____________

命令 5：下载文件
    curl -o test.json https://httpbin.org/json

    问题：当前目录下是否多了一个 test.json 文件？打开看看内容。
    你的答案：_____________
"""

# ==================== 参考答案 ====================
def check_exercise_4():
    print("=" * 50)
    print("【练习 4 参考答案】curl 练习")
    print("=" * 50)
    print("""
命令 1：origin 是你的公网 IP 地址
命令 2：args 中包含 {"name": "test", "course": "http"}
命令 3：data 字段是 '{"message":"hello"}'（你发送的 JSON 字符串）
命令 4：> 开头的是请求头（你发给服务器的），< 开头的是响应头（服务器返回的）
命令 5：应该多了一个 test.json 文件，内容是 httpbin 返回的示例 JSON
    """)


# ============================================================
# 【练习 5】Postman/Apifox 练习
# ============================================================
"""
如果你还没有安装 Postman 或 Apifox，请先安装：
- Apifox（推荐）：https://apifox.com/
- Postman：https://www.postman.com/

安装后完成以下任务：

任务 1：发送 GET 请求
    URL: https://jsonplaceholder.typicode.com/users
    问题：返回了多少个用户？第一个用户的名字是什么？
    你的答案：_____________

任务 2：发送 POST 请求
    URL: https://jsonplaceholder.typicode.com/posts
    Body (JSON):
    {
        "title": "我的第一篇博客",
        "body": "今天开始学习 Web 开发！",
        "userId": 1
    }
    问题：返回的状态码是多少？返回的 id 是多少？
    你的答案：_____________

任务 3：创建一个 Collection
    把任务 1 和任务 2 的请求保存到同一个 Collection 中，
    命名为 "Day 23 练习"。

    💡 提示：Collection 就像文件夹，帮你组织和管理 API 请求。
    以后做项目时，把所有接口都存到一个 Collection 里方便测试。

任务 4：设置环境变量
    在 Apifox/Postman 中创建一个环境变量：
    变量名：base_url
    变量值：https://jsonplaceholder.typicode.com

    然后把任务 1 的 URL 改为：{{base_url}}/users
    重新发送，确认能正常工作。

    💡 环境变量在切换开发/测试/生产环境时非常有用。
"""

# ==================== 参考答案 ====================
def check_exercise_5():
    print("=" * 50)
    print("【练习 5 参考答案】Postman/Apifox 练习")
    print("=" * 50)
    print("""
任务 1：返回 10 个用户，第一个用户名字是 "Leanne Graham"
任务 2：状态码 201，返回的 id 是 101
任务 3：操作题，无标准答案
任务 4：操作题，替换后 URL 应为 https://jsonplaceholder.typicode.com/users
    """)


# ============================================================
# 📌 今日 LeetCode 推荐
# ============================================================
#
# 1. LeetCode 232 - 用栈实现队列（Easy）
#    链接：https://leetcode.cn/problems/implement-queue-using-stacks/
#    关联：HTTP 请求也是"先进先出"的队列模型
#    思路提示：用两个栈，一个负责 push，一个负责 pop
#
# 2. LeetCode 225 - 用队列实现栈（Easy）
#    链接：https://leetcode.cn/problems/implement-stack-using-queues/
#    思路提示：用 collections.deque，push 时把前面的元素移到后面
#
# 💡 今天的题和栈/队列相关，是面试高频考点
# ============================================================


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    import sys

    print("\n" + "🚀 " * 15)
    print("  Day 23 观察 HTTP 请求 - 练习菜单")
    print("🚀 " * 15 + "\n")

    print("请选择要运行的练习：")
    print("  1 - 练习 2：启动本地 HTTP 服务器（在浏览器中测试）")
    print("  2 - 练习 3：requests 实验（自动运行）")
    print("  3 - 查看所有笔答题参考答案")
    print("  0 - 退出")
    print()

    choice = input("输入编号：").strip()

    if choice == "1":
        exercise_2_start_server()
    elif choice == "2":
        exercise_3_requests_experiments()
    elif choice == "3":
        check_exercise_1()
        check_exercise_4()
        check_exercise_5()
    elif choice == "0":
        print("退出。别忘了完成 F12 和 curl/Postman 的实操练习！")
    else:
        print("无效输入")
