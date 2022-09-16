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

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total:
        print()
