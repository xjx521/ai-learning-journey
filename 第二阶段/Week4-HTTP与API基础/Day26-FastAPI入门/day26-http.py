##web应用程序：遵循HTTP协议
import socket

sock = socket.socket()

sock.bind(("127.0.0.1", 8080))  # 端口
sock.listen(5)  # 最大排接数 从默认主动连接模式切换为被动监听模式

while True:
    conn, addr = (
        sock.accept()
    )  # 阻塞等待客户端链接 conn专门用来和当前这一个客户端收发数据 addr客户端地址
    data = conn.recv(1024)  # 接收客户端信息
    print("客户端发送的请求信息：\n", data)

    conn.send(
        b'HTTP/1.1 200 OK \r\n Server:xjx\r\nContent-type:application/json \r\n\r\n{"user_id":101}'
    )  # 必须是字节 并且按照相应头的格式 HTTP协议  状态码\r\n 相应头 \r\n\r\n 响应体
    conn.close()
