#!/usr/bin/python3
import socket,select
import struct,array
import threading
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
def handle_tcp(remote,_id):
        fdset = [remote,]
        while True:
            r, w, e = select.select(fdset, [], [],1)

            if remote in r:
                data = remote.recv(4096)
                
                if len(data)<= 0 :
                    break 

                send_data(sock,data,_id) 


def send_data(sock,data,_id):
    """
    Send ping to the target host
    """
    target_addr  =  '118.77.182.162'
    my_checksum = 0

    # Create a dummy heder with a 0 checksum.
    header = struct.pack("!BBHHH", 0, 0, my_checksum,_id, 0)
    

    # Get the checksum on the data and the dummy header.
    my_checksum = do_checksum(header + data)
    header = struct.pack("!BBHHH", 0, 0, my_checksum,_id,0)
    packet = header + data
    sock.sendto(packet, (target_addr, 1))
    print('send')

def recv_data(sock):
    '''把服务端取回的数据发送给客服端'''
    while True:
        try:
                data,addr = sock.recvfrom(4096) 
                print(data)
                icmp_head = data[20:28]
                data = data[28:]
                
                _type,code,chksum,_id,seqno = struct.unpack("!BBHHH",icmp_head) 
                print ("parse ICMP type=", _type,"code=",code, "_id=",_id,"seqno=",seqno)    
                print(_id)
               
                if id in remote_host.keys():
                   remote = remote_host[id]
                   remote.send(data) 
                t2 = threading.Thread(target=remote_send,args=(data,_id))
                t2.start()
        except:
            continue


def remote_send(data,_id):
     try:

        mode = data[1]
        addrtpye =data[3]
        
        if addrtpye == 1:
                addr = socket.inet_ntoa(data[4:-2])
        elif addrtpye ==3:
                addr_len = len(data[4:-2])
                addr = struct.unpack(str(addr_len)+'p',data[4:-2])
                addr = addr[0].decode('utf-8')

        port = struct.unpack('>H',data[-2:])
        print(port)
        reply = b"\x05\x00\x00\x01"

        try:
                if mode == 1:

                    remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    remote_host[_id] = remote
                    remote.connect((addr, port[0]))
                    print('Tcp connect to ',addr,port[0])
                else:
                    reply = b"\x05\x07\x00\x01" # Command not supported
                local = remote.getsockname()
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
        except socket.error:
                reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00' #Connection refused
        print(reply)
        send_data(sock,reply,_id)
        if reply[1] == 0:  # Success
                handle_tcp(remote,_id)

     except:
        print('sock error') 
if  __name__ =='__main__':
  global sock
  sock= socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname('icmp'))
  global remote_host
  remote_host = {}

  t1 = threading.Thread(target=recv_data,args=(sock,))
  t1.start()
