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
def printArquivo(lista):
    for i in range(0,len(lista)):
        lista[i] = "<br>"+lista[i]
    return lista
def criacaoCabecalhoServer(state,endereco,con):
    if state == "200":
        diretorio = []
        diretorio = listagemArquivosSistema(diretorio)
        if not endereco in diretorio and endereco != "/":
            cabecalhoHTTPError(404,"/404.html",con)
        elif endereco[-1] == "/":
            print endereco
            arq = open(pasta+"/dir.html",'w')
            diretorio = os.listdir(pasta+endereco)
            arq.write("<!DOCTYPE html><html><head><meta charset=\"UTF-8\"/><title> Diretorio: "+endereco+"</title></head><body><h1>"+endereco+"</h1>")
            arq.writelines(printArquivo(diretorio))
            arq.write("</body></html>")
            arq.close()
            cabecalhoHTTP(200,"/dir.html",con)
        else:
            cabecalhoHTTP(state,endereco,con)
    elif state == "500":
        cabecalhoHTTP500(con)
def contentType(arq):
    ext = arq.split(".")
    if ext[-1] == "html":
        return "text/HTML"
    elif ext[-1] == "txt":
        return "text/txt"
    elif ext[-1] == "jpg":
        return "image/jpg"
    elif ext[-1] == "png":
        return "image/png"
    elif ext[-1] == "gif":
        return "image/gif"
    elif ext[-1] == "ico":
        return "image/ico"
    elif ext[-1] == "css":
        return "text/css"
def cabecalhoHTTP(state,endereco,con):
    lenght = os.path.getsize(pasta+endereco)
    saida = "HTTP/1.1 "+str(state)+" OK\r\nContent-Type: "+ contentType(endereco)+"\r\nContent-Length: "+str(lenght)+"\r\n\r\n"
    arq = open(pasta+endereco,'r')
    dado = arq.read()
    con.send(saida+dado)
    con.close()
def cabecalhoHTTPError(state,endereco,con):
    saida = "HTTP/1.1 "+str(state)+" Not Found\r\nContent-Type: "+ contentType(endereco)+"\r\n\r\n"
    print "\n\n"+saida+"\n\n"
    arq = open(pasta+endereco,'r')
    dado = arq.read()
    con.send(saida+dado)
    con.close()
def cabecalhoHTTP500(con):
    saida = "HTTP/1.1 "+"500"+" Internal Server Error\r\nContent-Type: "+ contentType("/500.html")+"\r\n\r\n"
    print "\n\n"+saida+"\n\n"
    arq = open(pasta+"/500.html",'r')
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
        return state,endereco
    else:
        state = "500"
        return state,endereco

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)

        print cliente
        print msg
        state,endereco = tratamentoCabecalhoCliente(msg)
        criacaoCabecalhoServer(state,endereco,con)
        break
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
