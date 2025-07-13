import socket
import threading

clientes = {} 
registro_nomes = {}

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
    try:
        conn.send("Digite seu ID: ".encode())
        id_cliente = int(conn.recv(1024).decode())

        conn.send("Digite seu nome: ".encode())
        nome = conn.recv(1024).decode()

        registro_nomes[id_cliente] = nome
        clientes[id_cliente] = (conn, nome)

        print(f"[+] {nome} (ID {id_cliente}) conectado.")

        # Enviar lista de usuários online/offline
        status_msg = "\n--- STATUS DOS USUÁRIOS ---\n"
        for cid, nome_reg in registro_nomes.items():
            status = "Online" if cid in clientes else "Offline"
            status_msg += f"{nome_reg} (ID {cid}): {status}\n"
        status_msg += "---------------------------\n"
        conn.send(status_msg.encode())

        while True:
            msg = conn.recv(1024).decode()

            if msg.startswith("@"):
                try:
                    parte = msg.split(":", 1)
                    destino_id = int(parte[0][1:])
                    conteudo = parte[1]
                    enviar_para_cliente(destino_id, f"{nome} (privado): {conteudo}")
                except:
                    conn.send("Erro no formato da mensagem privada.\n".encode())
            else:
                broadcast(f"{nome}: {msg}", remetente_id=id_cliente)

    except Exception as e:
        print(f"[!] Cliente ID {id_cliente} desconectou. {e}")
    finally:
        if id_cliente in clientes:
            del clientes[id_cliente]
        conn.close()


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
