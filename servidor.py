import socket
import threading

clientes = {}  # id: (conn, nome)

def broadcast(mensagem, remetente_id=None):
    for cid, (conn, nome) in clientes.items():
        if cid != remetente_id:
            try:
                conn.send(mensagem.encode('utf-8'))
            except:
                pass

def enviar_para_cliente(destino_id, mensagem):
    if destino_id in clientes:
        conn, _ = clientes[destino_id]
        try:
            conn.send(mensagem.encode('utf-8'))
        except:
            pass

def handle_cliente(conn, addr):
    conn.send("Digite seu ID: ".encode())
    id_cliente = int(conn.recv(1024).decode())
    
    conn.send("Digite seu nome: ".encode())
    nome = conn.recv(1024).decode()

    clientes[id_cliente] = (conn, nome)
    print(f"[+] {nome} conectado com ID {id_cliente} ({addr})")
    conn.send(f"Bem-vindo, {nome}!\n".encode())

    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg.startswith("@"):
                try:
                    parte = msg.split(":", 1)
                    destino_id = int(parte[0][1:])
                    conteudo = parte[1]
                    enviar_para_cliente(destino_id, f"{nome} (privado): {conteudo}")
                except:
                    conn.send("Formato inválido. Use: @ID:mensagem\n".encode())
            else:
                broadcast(f"{nome}: {msg}", remetente_id=id_cliente)
        except:
            print(f"[-] {nome} desconectado.")
            del clientes[id_cliente]
            conn.close()
            break

def main():
    host = '127.0.0.1'
    port = 12345

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen()

    print(f"Servidor escutando em {host}:{port}")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=handle_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
