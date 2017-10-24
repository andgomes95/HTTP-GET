import socket
import thread
import sys
try:
    pasta = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print "Falta argumentos para o servidor"
    sys.exit(0)

HOST = ''

def tratamentoCabecalhoCliente(msg):
    cabecalho = msg.split("\r\n")
    UserAgent = " "
    Accept = " "
    AcceptLanguage = " "
    AcceptEncoding = " "
    Connection =  " "
    endereco = " "
    if cabecalho[0].split(" ")[0] == "GET" and cabecalho[0].split(" ")[2]=="HTTP/1.1":
        endereco = cabecalho[0].split(" ")[1]
        print endereco
        for i in range(1,len(cabecalho)):
            if "Accept" == cabecalho[i].split(":")[0]:
                for j in range(1,len(cabecalho[i].split(":"))):
                    Accept = Accept +cabecalho[i].split(":")[j]
                print Accept
            if "Accept-Language" == cabecalho[i].split(":")[0]:
                for j in range(1,len(cabecalho[i].split(":"))):
                    AcceptLanguage = AcceptLanguage + cabecalho[i].split(":")[j]
                print AcceptLanguage
            if "Accept-Encoding" == cabecalho[i].split(":")[0]:
                for j in range(1,len(cabecalho[i].split(":"))):
                    AcceptEncoding = AcceptEncoding + cabecalho[i].split(":")[j]
                print AcceptEncoding
            if "User-Agent" == cabecalho[i].split(":")[0]:
                for j in range(1,len(cabecalho[i].split(":"))):
                    UserAgent = UserAgent + cabecalho[i].split(":")[j]
                print UserAgent
            if "Connection" == cabecalho[i].split(":")[0]:
                for j in range(1,len(cabecalho[i].split(":"))):
                    Connection = Connection + cabecalho[i].split(":")[j]
                print Connection
    #else:
    #   Badrequest 400

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        print msg
        tratamentoCabecalhoCliente(msg)

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
