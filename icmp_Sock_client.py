import socket,struct,select,array
import threading
import random


def do_checksum(packet):
        '''ICMP 报文效验和计算方法'''
        if len(packet) & 1:
            packet = packet + b'\0'
        words = array.array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)

        return (~sum) & 0xffff




def send_client(sock):
    '''把服务端取回的数据发送给客服端'''

    while True:
            data,addr = sock.recvfrom(4086)
            icmp_head = data[20:28]
            data = data[28:]
            _type,code,chksum,id,seqno = struct.unpack("!BBHHH",icmp_head)
            print ("parse ICMP type=", _type,"code=",code, "_id=",id,"seqno=",seqno)
            if data[1] == 0:
                client = client_host[id]
                client.send(data)
            else:
                client = client_host[id]
                if client.send(data) <= 0: continue


def send_data(sock,data,id):
    """
    Send ping to the target host
    """
    target_addr  =  '172.110.31.7'
    my_checksum = 0

    # Create a dummy heder with a 0 checksum.
    header = struct.pack("!BBHHH", 8, 56, my_checksum,id,0)


    # Get the checksum on the data and the dummy header.
    my_checksum = do_checksum(header + data)
    header = struct.pack("!BBHHH", 8, 56, my_checksum,id,0)
    packet = header + data

    sock.sendto(packet, (target_addr, 1))
def run(client):

        id = random.randint(1,10000)
        print('id:',id)

        client_host[id] = client
        data = client.recv(262)
        client.send(b'\x05\x00')
        data = client.recv(1000)
        print(data)
        send_data(sock,data,id)
        #send_server(client,id)
        fdset = [client,]
        while True:

            data = client.recv(4086)

            if len(data)<= 0 :
                break
            print(data)
            send_data(sock,data,id)


if __name__ =='__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname('icmp'))
    s.bind(('',1080))
    s.listen(10)
    global client_host
    client_host = {}
    t2 = threading.Thread(target=send_client,args=(sock,))
    t2.start()
    while True:
        client, addr = s.accept()
        t1 = threading.Thread(target=run,args=(client,))
        t1.start()


