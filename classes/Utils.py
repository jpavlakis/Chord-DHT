import random
import socket
import struct
import hashlib
import math

def generateIp(nodes):
    """
    Generates a unique IP Address for every node.
    """
    ip_exists = False
    ipAddress = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    for node in nodes:
        if(node.getIpAddress() == ipAddress):
            ip_exists = True
            break
    while(ip_exists):
        ipAddress = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        for node in nodes:
            if(node.getIpAddress() == ipAddress):
                ip_exists = True
                break
        else:
            ip_exists = False
    
    return ipAddress

def generateHash(value, m):
    """
    Hashing the value using sha1 algorithm and from the 160 bit
    output we only take the m last bits.
    """
    hashed_ip_hex = hashlib.sha1(value.encode('utf-8')).hexdigest()
    hashed_ip_bin = bin(int(hashed_ip_hex, 16))
    return int(hashed_ip_bin[-m:], 2)

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '\r'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total:
        print()

def closest_power2_exponent(x):
    """
    Returns the exponent of the closest power of 2 to the input x
    """
    return math.ceil(math.log(x,2))

