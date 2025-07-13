import socket           # Biblioteca para comunicação de rede (sockets TCP/IP)
import threading        # Biblioteca para rodar tarefas em paralelo (threads)

# Função que fica rodando em segundo plano para receber mensagens do servidor
def receber_mensagens(sock):
    while True:
        try:
            # Recebe a mensagem enviada pelo servidor
            msg = sock.recv(1024).decode()
            print(msg)  # Exibe a mensagem no terminal do cliente
        except:
            # Caso ocorra um erro (ex: desconexão), exibe aviso e encerra a thread
            print("Erro ao receber mensagem.")
            break

# Função principal que executa o cliente
def main():
    host = '127.0.0.1'       # Endereço IP do servidor (localhost)
    port = 12345             # Porta usada pelo servidor (mesma do servidor.py)

    # Cria o socket do cliente (protocolo TCP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta esse cliente ao servidor
    cliente.connect((host, port))

    # Cria uma thread paralela para receber mensagens sem travar o input do usuário
    threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True).start()

    # Loop principal: envia mensagens digitadas pelo usuário para o servidor
    while True:
        msg = input()               # Espera o usuário digitar uma mensagem
        cliente.send(msg.encode()) # Envia a mensagem codificada para o servidor

# Executa a função main se este arquivo for o programa principal
if __name__ == "__main__":
    main()
