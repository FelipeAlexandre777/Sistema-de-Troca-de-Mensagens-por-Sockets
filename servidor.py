import socket            # Para comunicação entre computadores
import threading         # Para lidar com múltiplos clientes ao mesmo tempo

clientes = {}            # Dicionário com clientes online: {id: (conexao, nome)}
registro_nomes = {}      # Dicionário com todos que já se conectaram: {id: nome}

# Envia uma mensagem para todos os clientes online, exceto o remetente
def broadcast(mensagem, remetente_id=None):
    for cid, (conn, nome) in clientes.items():
        if cid != remetente_id:
            try:
                conn.send(mensagem.encode('utf-8'))
            except:
                pass  # Se falhar, ignora

# Envia uma mensagem privada para um cliente específico pelo ID
def enviar_para_cliente(destino_id, mensagem):
    if destino_id in clientes:
        conn, _ = clientes[destino_id]
        try:
            conn.send(mensagem.encode('utf-8'))
        except:
            pass  # Se falhar, ignora

# Função que lida com a comunicação de um cliente
def handle_cliente(conn, addr):
    try:
        # Solicita ID do cliente
        conn.send("Digite seu ID: ".encode())
        id_cliente = int(conn.recv(1024).decode())

        # Solicita nome do cliente
        conn.send("Digite seu nome: ".encode())
        nome = conn.recv(1024).decode()

        # Armazena o nome no histórico e adiciona na lista de online
        registro_nomes[id_cliente] = nome
        clientes[id_cliente] = (conn, nome)

        print(f"[+] {nome} (ID {id_cliente}) conectado.")

        # Envia a lista de usuários online/offline para o cliente
        status_msg = "\n--- STATUS DOS USUÁRIOS ---\n"
        for cid, nome_reg in registro_nomes.items():
            status = "Online" if cid in clientes else "Offline"
            status_msg += f"{nome_reg} (ID {cid}): {status}\n"
        status_msg += "---------------------------\n"
        conn.send(status_msg.encode())

        # Loop principal do cliente
        while True:
            msg = conn.recv(1024).decode()

            # Se a mensagem for privada (começa com @)
            if msg.startswith("@"):
                try:
                    parte = msg.split(":", 1)
                    destino_id = int(parte[0][1:])   # Ex: @2
                    conteudo = parte[1]              # Ex: mensagem
                    enviar_para_cliente(destino_id, f"{nome} (privado): {conteudo}")
                except:
                    conn.send("Erro no formato da mensagem privada.\n".encode())
            else:
                # Envia para todos (broadcast)
                broadcast(f"{nome}: {msg}", remetente_id=id_cliente)

    except Exception as e:
        print(f"[!] Cliente ID {id_cliente} desconectou. {e}")
    finally:
        # Remove cliente da lista e fecha conexão
        if id_cliente in clientes:
            del clientes[id_cliente]
        conn.close()

# Função principal do servidor
def main():
    host = '127.0.0.1'    # IP local (localhost)
    port = 12345          # Porta de escuta

    # Cria socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))  # Liga o IP e porta
    servidor.listen()            # Começa a escutar conexões

    print(f"Servidor escutando em {host}:{port}")

    # Aceita múltiplas conexões
    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=handle_cliente, args=(conn, addr))
        thread.start()

# Executa se for o arquivo principal
if __name__ == "__main__":
    main()
