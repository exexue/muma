import socket,struct,select
import threading

def handle_tcp(sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [],1)
            if sock in r:
                data = sock.recv(4096)
                #print(data)
                #print('sock')
                if remote.send(data) <= 0: break
            if remote in r:
                data = remote.recv(4096)
                #print(data)
                #print('remote')
                if sock.send(data) <= 0: break

def run(client):

    try:
        data = client.recv(262)
        #print(data)
        client.send(b'\x05\x00')
        data = client.recv(1000)
        mode = data[1]
        addrtpye = data[3]

        if addrtpye == 1:
            addr = socket.inet_ntoa(data[4:-2])
        elif addrtpye ==3:
            addr_len = len(data[4:-2])
            addr = struct.unpack(str(addr_len)+'p',data[4:-2])
            addr = addr[0].decode('utf-8')
        port = struct.unpack('>H',data[-2:])
        print(addr)
        reply = b"\x05\x00\x00\x01"
        try:
            if mode == 1:

                remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                remote.connect((addr, port[0]))
                print('Tcp connect to ',addr,port[0])
            else:
                reply = b"\x05\x07\x00\x01" # Command not supported
            local = remote.getsockname()
            reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
        except:
            reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00' #Connection refused
        client.send(reply)
        if reply[1] == 0:  # Success
            handle_tcp(client, remote)
    except:
            print('socket error')


if __name__ =='__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',1080))
    s.listen(10)

    while True:
        client, addr = s.accept()
        t1 = threading.Thread(target=run,args=(client,))
        t1.start()


