import socket

def get_ip():
    # 创建 UDP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 连接到外部服务器（这里用 Google DNS，不实际发送数据）
    s.connect(("8.8.8.8", 80))
    # 获取套接字的本地 IP
    ip = s.getsockname()[0]
    s.close()  # 关闭套接字

    return str(ip)

get_ip()