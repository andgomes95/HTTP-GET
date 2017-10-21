import socket
import sys
HOST = '127.0.0.1'     # Endereco IP do Servidor
if len(sys.argv) == 2:
    PORT = int(sys.argv[1])
else:
    PORT = 80            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = raw_input()
#comandos = msg.split(" ")
#if len(comandos) == 3:
#    PORT = int(comandos[2])
try:
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send (msg)
    dado = tcp.recv(1048576)
    if dado == "404":
        print "ERROR 404 \n NOT FOUND"
    else:
        arq = open("page.html",'w')
        arq.write(dado)
        arq.close()
        tcp.close()
except:
    print "ERROR 500\n\nINTERNAL SERVER ERROR"
