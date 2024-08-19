p = 2800926522328793
q = 5680476311489549

# Virat's public key
N = 15910596760311511967802161284357         #(p*q)
e = 35421826192615868656164957915281

x = 0
y = 1

#extended Euclidean Algorithm
def gcdExtended(a, b):
    global x, y
    if (a == 0):
        x = 0
        y = 1
        return b
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y
    x = y1 - (b // a) * x1
    y = x1
    return gcd
 
 
def modInverse(A, M):
    g = gcdExtended(A, M)
    if (g != 1):
        print("Inverse doesn't exist")
    else:
        res = (x % M + M) % M
        return res
    
d = modInverse(e, (p-1)*(q-1))

import socket

bufferSize  = 4096

localIP     = "127.0.0.1"
localPort   = 21603

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    address = bytesAddressPair[1]
    message = message.split(" ")
    secret_message = ""
    for i in range (0, len(message)-1):
        message[i] = int(message[i])
        message[i] = pow(message[i], d, N)
        message[i] = chr(message[i])
        secret_message += message[i]
    
    print(secret_message)
