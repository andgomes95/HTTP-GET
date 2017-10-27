import socket
import thread
import sys
import os
try:
    pasta = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print "Falta argumentos para o servidor"
    sys.exit(0)

HOST = ''
def listagemArquivosSistema(diretorio):
    diretorio = tratamentoListaArquivos(os.listdir(pasta+"/"))
    for i in range(0,len(diretorio)):
        if "/" == diretorio[i][-1]:
            dirr = tratamentoListaArquivos(os.listdir(pasta+diretorio[i]))
            for j in range(0,len(dirr)):
                if dirr[j][-1] == "/":
                    dirr[j] = dirr[j].replace("/","")
                    dirr[j] = dirr[j] + "/"
                else:
                    dirr[j] = dirr[j].replace("/","")
                dirr[j] = diretorio[i]+dirr[j]
            diretorio = diretorio + dirr
    return diretorio
def criacaoCabecalhoServer(state,endereco,con):
    if state == "200":
        diretorio = []
        diretorio = listagemArquivosSistema(diretorio)

        if not endereco in diretorio:
            state = "401"
            print "deu ruim"
        else:
            print "deu bom"
            cabecalhoHTTP(state,endereco,con)
    elif state == "400":
        print "oho"
def cabecalhoHTTP(state,endereco,con):
    lenght = os.path.getsize(pasta+endereco)
    saida = "HTTP/1.1 "+str(state)+" OK\nContent-Type: text/HTML\nContent-Length :"+str(lenght)+"\n\n"
    arq = open(pasta+endereco,'r')
    dado = arq.read()
    con.send(saida+dado)
    con.close()

def tratamentoListaArquivos(diretorio):
    for i in range(0,len(diretorio)):
        diretorio[i] = "/"+diretorio[i]
        if not "." in diretorio[i]:
            diretorio[i] = diretorio[i] + "/"
    return diretorio
def tratamentoCabecalhoCliente(msg):
    cabecalho = msg.split("\r\n")
    UserAgent = " "
    Accept = " "
    AcceptLanguage = " "
    AcceptEncoding = " "
    Connection =  " "
    endereco = " "
    if cabecalho[0].split(" ")[0] == "GET" and cabecalho[0].split(" ")[2]=="HTTP/1.1":
        state = "200"
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
        return state,endereco,Accept,AcceptLanguage,AcceptEncoding,UserAgent,Connection
    else:
        state = "400"
        return state,endereco,Accept,AcceptLanguage,AcceptEncoding,UserAgent,Connection
    #   Badrequest 400
    #   sys.exit(0)

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)
        if not msg: break
        print cliente
        print msg
        state,endereco,accept,acceptLanguage,acceptEnconding,userAgent,connection = tratamentoCabecalhoCliente(msg)
        criacaoCabecalhoServer(state,endereco,con)
        #con.close()

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
