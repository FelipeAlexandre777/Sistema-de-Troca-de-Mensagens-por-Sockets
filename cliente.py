import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            print("Erro ao receber mensagem.")
            break

def main():
    host = '127.0.0.1'
    port = 12345

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))

    # Thread para receber mensagens
    threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True).start()

    while True:
        msg = input()
        cliente.send(msg.encode())

if __name__ == "__main__":
    main()
