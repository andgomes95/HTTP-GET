import socket
import thread

HOST = ''              # Endereco IP do Servidor
PORT = 80            # Porta que o Servidor esta
def transferenciaArquivo(endereco):
    print endereco
def abstracaoComandos(msg):
    print msg
    comandos = msg.split(" ")
    if comandos[0] != "navegador":
        print "Funcao nao implementada"
    else:
        transferenciaArquivo(msg[1])

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        abstracaoComandos(msg)

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
