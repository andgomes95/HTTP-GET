import socket
import sys
if len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    HOST = sys.argv[1]
    PORT = 80
else:
    print "Faltam argumentos"
    sys.exit()
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    dest = (HOST, PORT)
    tcp.connect(dest)
    msg = raw_input()
    tcp.send (msg)
    dado = tcp.recv(1048576)
    if dado == "Funcao nao implementada":
        print "Funcao nao implementada"
    else:
        arq = open("page.html",'w')
        arq.write(dado)
        arq.close()
    tcp.close()
except:
    arq = open("500.html",'r')
    arq1 = open("page.html",'w')
    dado = arq.read()
    arq1.write(dado)
    arq.close()
    tcp.close()
