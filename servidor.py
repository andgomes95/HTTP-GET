import socket
import thread
import sys
try:
    pasta = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print "Falta argumentos para o servidor"
    sys.exit(0)

HOST = '0.0.0.0'              # Endereco IP do Servidor
def transferenciaArquivo(con,endereco):
    try:
        arq = open(pasta + "/" + endereco,'r')
        dado = arq.read()
        con.send(dado)
        arq.close()
    except:
        dado = "404"
        con.send(dado)

def abstracaoComandos(con,msg):
    print msg
    comandos = msg.split(" ")
    if comandos[0] != "GET":
        print "Funcao nao implementada"
    else:
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
    print con
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
