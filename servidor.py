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

HOST = '0.0.0.0'              # Endereco IP do Servidor
def transferenciaArquivo(con,endereco):
    end = pasta + endereco
    diretorios = os.listdir(pasta+"/")
    for i in range(0,len(diretorios)):
        diretorios[i] ="/"+ diretorios[i]
        if not "." in diretorios[i]:
            diretorios[i] = diretorios[i] + "/"
    if endereco in diretorios:
        cabecalho = "HTTP/1.1 200 OK\nCache-Control: no-cache\nKeep-Alive: timeout=3, max=100\nConnection: Keep-Alive\nTransfer-Encoding: chunked\nContent-Type: ahtml; charset=iso-8859-1"
        if endereco[-1] == "/":
            dir = pasta+endereco
            print dir
            conteudo = os.listdir(dir)
            saida = "<!DOCTYPE html>\n            <html>\n                <head>\n                    <meta charset=\"UTF-8\"/>\n                    <title>"
            saida = saida + endereco
            saida = saida + "</title>\n                </head>\n                <body>\n"
            print len(conteudo)
            for i in range(0,len(conteudo)):
                saida = saida+"<br>"+conteudo[i]+"\n"
            saida = saida + "</body>\n</html>"
            print saida
            con.send(cabecalho+saida)
            con.close()
        else:
            arq = open(end,'r')
            dado = arq.read()
            con.send(cabecalho+dado)
            arq.close()
            con.close()
    else:
        arq = open("404.html",'r')
        dado = arq.read()
        con.send(cabecalho+dado)
        arq.close()
        con.close()


def abstracaoComandos(con,msg):
    print msg
    comandos = msg.split(" ")
#    if comandos[0] != "GET":
#        dado = "Funcao nao implementada"
#        con.send(dado)
#    else:
    transferenciaArquivo(con,comandos[1])

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        abstracaoComandos(con,msg)

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
