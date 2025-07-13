import socket           # Biblioteca para comunicação de rede (Sockets)
import threading        # Biblioteca para rodar tarefas em paralelo (threads)

# Função que fica ouvindo mensagens do servidor
def receber_mensagens(sock):
    while True:
        try:
            # Recebe dados do servidor e imprime na tela
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            # Se der erro, imprime mensagem e encerra
            print("Erro ao receber mensagem.")
            break

def main():
    host = '127.0.0.1'       # Endereço IP do servidor (localhost)
    port = 12345             # Porta do servidor (a mesma do servidor.py)

    # Cria o socket cliente (TCP/IP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    cliente.connect((host, port))

    # Cria uma thread para escutar mensagens do servidor em paralelo
    threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True).start()

    # Enquanto o usuário digitar mensagens, envia para o servidor
    while True:
        msg = input()
        cliente.send(msg.encode())

# Executa o programa principal se for o arquivo principal
if __name__ == "__main__":
    main()
