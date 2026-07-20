"""
本地版 httpbin —— Day 23 练习作品
================================
用 Python 标准库实现一个简易的 HTTP 调试服务器，
用来替代不稳定的 httpbin.org，随时随地练习 HTTP 请求。

运行方式：
    python my_httpbin.py
然后在浏览器访问 http://localhost:8888/ 或者用 curl/Postman 发请求

涵盖 6 个最常用端点：
    GET  /            欢迎页 + 使用说明
    GET  /get         回显请求头 + URL 参数
    POST /post        回显请求体（JSON / 表单 / 纯文本）
    GET  /status/<code>  返回指定状态码（如 /status/404）
    GET  /headers     只回显请求头
    GET  /delay/<n>   延迟 n 秒后响应（测试超时）
"""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class MyHttpbinHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求，模仿 httpbin.org 的核心功能"""

    # --------------------------------------------------
    # 工具方法：统一构造 JSON 响应
    # --------------------------------------------------
    def _send_json(self, data, status=200):
        """
        把 Python 字典/列表转成 JSON 发回给客户端
        - data:   要返回的数据（字典或列表）
        - status: HTTP 状态码，默认 200
        """
        # 1. 把数据转成 JSON 字符串，再编码成 bytes（网络传输要字节）
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

        # 2. 发送状态行，比如 "HTTP/1.1 200 OK"
        self.send_response(status)

        # 3. 告诉浏览器：我返回的是 JSON，用 UTF-8 编码
        self.send_header("Content-Type", "application/json; charset=utf-8")
        # Content-Length 让浏览器知道要收多少字节，避免截断
        self.send_header("Content-Length", str(len(body)))
        # 加一个自定义头，演示"服务器可以随便给自己加标签"
        self.send_header("X-Powered-By", "我的本地 httpbin")

        # 4. 响应头到此结束，后面就是响应体
        self.end_headers()

        # 5. 把字节数据写出去
        self.wfile.write(body)

    # --------------------------------------------------
    # 工具方法：收集请求信息（请求头、参数、请求体）
    # --------------------------------------------------
    def _collect_request_info(self):
        """
        把当前请求的各种信息打包成一个字典，
        等下转成 JSON 返回，让你看清楚"我发的请求长什么样"
        """
        # 解析 URL：比如 /get?name=张三&age=20
        parsed = urlparse(self.path)

        # parse_qs 把 ? 后面的参数解析成字典
        # 例如 {'name': ['张三'], 'age': ['20']}
        args = parse_qs(parsed.query)
        # 把每个值从列表拍平成字符串（httpbin 风格）
        # {'name': ['张三']} → {'name': '张三'}
        args_flat = {k: v[0] if len(v) == 1 else v for k, v in args.items()}

        # 把请求头转成普通字典（self.headers 是个特殊对象）
        headers = {k: v for k, v in self.headers.items()}

        return {
            "method": self.command,           # GET / POST / PUT ...
            "path": self.path,                # 完整路径（含 ?参数）
            "url_path": parsed.path,          # 纯路径（不含参数）
            "args": args_flat,                # URL 参数
            "headers": headers,               # 请求头
            "origin": self.client_address[0], # 客户端 IP
        }

    # --------------------------------------------------
    # 工具方法：读取请求体（POST/PUT 时才有）
    # --------------------------------------------------
    def _read_body(self):
        """
        读取客户端发来的请求体（比如 POST 提交的 JSON）
        - 先根据 Content-Length 知道要读多少字节
        - 如果没有 Content-Length，返回 None
        """
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            return None
        # 读指定字节数的数据
        raw = self.rfile.read(int(content_length))
        # 转成字符串（假设是 UTF-8）
        return raw.decode("utf-8")

    # ==================================================
    # 处理 GET 请求
    # ==================================================
    def do_GET(self):
        """所有 GET 请求都走这里，根据路径分发到不同处理函数"""
        parsed = urlparse(self.path)
        path = parsed.path  # 只看路径部分，不管参数

        # ---------- 欢迎页 ----------
        if path == "/":
            return self._handle_index()

        # ---------- /get：回显请求信息 ----------
        if path == "/get":
            return self._handle_get()

        # ---------- /headers：只回显请求头 ----------
        if path == "/headers":
            return self._handle_headers()

        # ---------- /status/<code>：返回指定状态码 ----------
        if path.startswith("/status/"):
            # 从路径里抠出状态码数字，比如 /status/404 → 404
            code_str = path.replace("/status/", "")
            return self._handle_status(code_str)

        # ---------- /delay/<n>：延迟 n 秒 ----------
        if path.startswith("/delay/"):
            sec_str = path.replace("/delay/", "")
            return self._handle_delay(sec_str)

        # ---------- 其他路径：404 ----------
        self._send_json(
            {"error": "路径不存在", "path": path,
             "hint": "试试 /get、/headers、/status/404、/delay/3"},
            status=404
        )

    # ==================================================
    # 处理 POST 请求
    # ==================================================
    def do_POST(self):
        """所有 POST 请求都走这里"""
        parsed = urlparse(self.path)
        if parsed.path == "/post":
            return self._handle_post()
        self._send_json({"error": "POST 只支持 /post"}, status=404)

    # ==================================================
    # 处理 PUT 请求（顺便支持一下，练习 CRUD 会用到）
    # ==================================================
    def do_PUT(self):
        """PUT 请求，功能跟 POST 一样，只是 method 字段不同"""
        parsed = urlparse(self.path)
        if parsed.path == "/put":
            return self._handle_post(method_field="PUT")
        self._send_json({"error": "PUT 只支持 /put"}, status=404)

    # ==================================================
    # 处理 DELETE 请求
    # ==================================================
    def do_DELETE(self):
        """DELETE 请求"""
        parsed = urlparse(self.path)
        if parsed.path == "/delete":
            return self._handle_post(method_field="DELETE")
        self._send_json({"error": "DELETE 只支持 /delete"}, status=404)

    # ==================================================
    # 各个端点的处理函数
    # ==================================================

    def _handle_index(self):
        """GET / —— 欢迎页，告诉你能用哪些端点"""
        # 注意：这里返回的是 HTML 字符串，不是 JSON
        html = """
        <h1>🎉 欢迎来到我的本地 httpbin！</h1>
        <p>可用端点：</p>
        <ul>
            <li><b>GET /get</b> — 回显请求头 + URL 参数</li>
            <li><b>POST /post</b> — 回显请求体</li>
            <li><b>PUT /put</b> — 回显 PUT 请求体</li>
            <li><b>DELETE /delete</b> — 回显 DELETE 请求</li>
            <li><b>GET /headers</b> — 只回显请求头</li>
            <li><b>GET /status/&lt;code&gt;</b> — 返回指定状态码</li>
            <li><b>GET /delay/&lt;n&gt;</b> — 延迟 n 秒</li>
        </ul>
        <p>试试：<a href="/get?name=张三&age=20">/get?name=张三&amp;age=20</a></p>
        """
        # 返回 HTML 要用 text/html，不是 application/json
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_get(self):
        """GET /get —— 把你发的请求信息原样返回"""
        info = self._collect_request_info()
        self._send_json(info)

    def _handle_post(self, method_field="POST"):
        """
        POST /post（也兼容 PUT/DELETE）
        除了回显请求信息，还要回显请求体（form 或 json）
        """
        info = self._collect_request_info()
        info["method"] = method_field  # 覆盖成真实方法

        # 读取请求体
        raw_body = self._read_body()

        # 尝试把请求体解析成 JSON（如果是 JSON 格式）
        # 解析失败就当普通字符串
        content_type = self.headers.get("Content-Type", "")
        info["data"] = raw_body  # 原始字符串
        if raw_body:
            if "json" in content_type:
                try:
                    info["json"] = json.loads(raw_body)
                except json.JSONDecodeError:
                    info["json"] = None
            elif "x-www-form-urlencoded" in content_type:
                # 表单数据也解析成字典
                info["form"] = {
                    k: v[0] if len(v) == 1 else v
                    for k, v in parse_qs(raw_body).items()
                }
            else:
                info["json"] = None

        self._send_json(info)

    def _handle_headers(self):
        """GET /headers —— 只回显请求头"""
        headers = {k: v for k, v in self.headers.items()}
        self._send_json({"headers": headers})

    def _handle_status(self, code_str):
        """
        GET /status/<code>
        比如 /status/404 返回 404，/status/500 返回 500
        """
        try:
            code = int(code_str)
        except ValueError:
            # 传的不是数字，比如 /status/abc
            return self._send_json(
                {"error": "状态码必须是数字", "you_sent": code_str},
                status=400  # 400 = Bad Request，客户端的错
            )

        # 返回指定状态码 + 一句提示
        self._send_json(
            {"status": code, "message": f"这是你请求的 {code} 响应"},
            status=code
        )

    def _handle_delay(self, sec_str):
        """
        GET /delay/<n>
        故意等 n 秒再响应，用来测试你的超时处理逻辑
        """
        try:
            sec = int(sec_str)
        except ValueError:
            return self._send_json(
                {"error": "秒数必须是数字", "you_sent": sec_str},
                status=400
            )

        # 限制最大延迟，避免误操作等太久
        if sec > 10:
            return self._send_json(
                {"error": "最多只能延迟 10 秒", "you_sent": sec},
                status=400
            )

        # 真的要睡 n 秒！
        time.sleep(sec)

        self._send_json({
            "delay": sec,
            "message": f"我睡了 {sec} 秒才回复你",
        })


# ==================================================
# 启动服务器
# ==================================================
def main():
    host = "127.0.0.1"
    port = 8888
    server = HTTPServer((host, port), MyHttpbinHandler)
    print(f"🚀 本地 httpbin 启动成功！")
    print(f"👉 浏览器访问：http://{host}:{port}/")
    print(f"👉 或用 curl：  curl http://{host}:{port}/get?name=张三")
    print(f"按 Ctrl+C 停止服务器")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        server.server_close()


if __name__ == "__main__":
    main()
