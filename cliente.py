import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 80            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = raw_input()
#comandos = msg.split(" ")
#if len(comandos) == 3:
#    PORT = int(comandos[2])
dest = (HOST, PORT)
tcp.connect(dest)
print 'Para sair use CTRL+X\n'
tcp.send (msg)
tcp.close()
