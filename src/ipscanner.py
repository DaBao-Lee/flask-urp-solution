import os
import platform
import threading

# 设置你的子网地址，比如 192.168.1
subnet = "172.22.92"
# 扫描范围
start = 1
end = 254

# 检查系统类型
param = "-n" if platform.system().lower() == "windows" else "-c"

# 定义 ping 函数
def ping(ip):
    response = os.system(f"ping {param} 1 -w 100 {ip} >nul" if param == "-n"
                         else f"ping {param} 1 -W 1 {ip} >/dev/null 2>&1")
    if response == 0:
        print(f"[+] 在线：{ip}")

# 使用多线程加速扫描
threads = []
for i in range(start, end + 1):
    ip = f"{subnet}.{i}"
    thread = threading.Thread(target=ping, args=(ip,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
