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
def connect(HOST,PORT):

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = HOST.replace("http://","")
    pastas = HOST.split("/")
    HOST = socket.gethostbyname(pastas[0])
    dest = (HOST, PORT)
    tcp.connect(dest)
    return pastas,HOST,tcp
def requisicao(pastas,tcp):
    GET = ""
    for i in range(1,len(pastas)):
        GET = GET+"/"+pastas[i]
    msg = "GET "+GET
    msg = msg + " HTTP/1.1\r\nUser-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3\r\nHost: "+HOST+":"+str(PORT)+"\r\nAccept-Language: pt-br\r\n\r\n"
    tcp.send (msg)
def separaCabecalho():
    rsp = tcp.recv(1048576)
    res = rsp.split("\n\r\n")
    return res[0],res[1]
def infoCabecalho(cabecalho):
    itens = cabecalho.split("\n")
    itens = cabecalho.split("\r")
    for i in range(0,len(itens)):
        if "HTTP/1.1" in itens[i]:
            aux = itens[i].split(" ")
            if aux[1] == "200":
                print aux
            else:
                print aux[1]+" "+aux[2]
                sys.exit(0)
        elif "Content-Length" in itens[i]:
            aux = itens[i].split(" ")
            if "\r" in aux[1]:
                length = int(aux[1].replace("\r",""))
            else:
                length = int(aux[1])
    return length
pastas,HOST,tcp = connect(HOST,PORT)
requisicao(pastas,tcp)
cabecalho,corpo = separaCabecalho()
print len(cabecalho)
length = infoCabecalho(cabecalho)
print length
arq1 = open("page.html",'w')
arq1.write(corpo)
arq1.close()
tcp.close()
