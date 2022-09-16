import random
import socket
import struct
import hashlib

def generateIp(nodes):
    """
    Generates a unique IP Address for every node.
    """
    ip_exists = False
    ipAddress = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    for node in nodes:
        if(node.ipAddress==ipAddress):
            ip_exists = True
            break
    while(ip_exists):
        ipAddress = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        for node in nodes:
            if(node.ipAddress==ipAddress):
                ip_exists = True
                break
        else:
            ip_exists = False
    
    return ipAddress

def hashing(value, m):
    """
    Hashing the value using sha1 algorithm and from the 160 bit
    output we only take the m last bits.
    """
    hashed_ip_hex = hashlib.sha1(value.encode('utf-8')).hexdigest()
    hashed_ip_bin = bin(int(hashed_ip_hex, 16))
    return int(hashed_ip_bin[-m:], 2)