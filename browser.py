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
    if len(pastas) == 1:
        GET = "/"
    for i in range(1,len(pastas)):
        GET = GET+"/"+pastas[i]
    msg = "GET "+GET
    msg = msg + " HTTP/1.1\r\nUser-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3\r\nHost: "+HOST+"\r\nAccept-Language: en,pt-br\r\nConnection: close\r\n\r\n"
    tcp.send (msg)
def separaCabecalho():
    rsp = tcp.recv(4096)
    res = rsp.split("\n\r\n")
    saida = ""
    for i in range(1,len(res)):
        saida = saida + res[i]
    return res[0],saida
def restoCorpo():
    rsp = tcp.recv(4096)
    return rsp
def infoCabecalho(cabecalho):
    itens = cabecalho.split("\n")
    itens = cabecalho.split("\r")
    length = 1024
    for i in range(0,len(itens)):
        if "HTTP/1.1" in itens[i] or "HTTP/1.0" in itens[i]:
            aux = itens[i].split(" ")
            if aux[1] == "200":
                print aux[2]
            else:
                saida = ""
                for i in range(1,len(aux)):
                    saida = saida + aux[i]+" "
                print saida
                sys.exit(0)
        elif "Content-Length" in itens[i]:
            aux = itens[i].split(" ")
            print aux
            if "\r" in aux[1]:
                length = int(aux[1].replace("\r",""))
            else:
                length = int(aux[1])
    return length
pastas,HOST,tcp = connect(HOST,PORT)
requisicao(pastas,tcp)
cabecalho,corpo = separaCabecalho()
length = infoCabecalho(cabecalho)
tam = 4096
while length*1024 > tam:
    corpo = corpo + restoCorpo()
    tam = tam + tam
print corpo
arq1 = open("page.html",'w')
arq1.write(corpo)
arq1.close()
tcp.close()
