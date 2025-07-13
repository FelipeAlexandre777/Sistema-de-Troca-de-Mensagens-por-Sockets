import socket            # Biblioteca para comunicação entre computadores via rede
import threading         # Biblioteca para trabalhar com múltiplas conexões simultâneas (threads)

clientes = {}            # Dicionário com os clientes ONLINE -> {id: (conexao, nome)}
registro_nomes = {}      # Histórico com todos os usuários que já entraram (inclusive OFFLINE) -> {id: nome}

# Função que envia uma mensagem para TODOS os clientes online, exceto o remetente
def broadcast(mensagem, remetente_id=None):
    for cid, (conn, nome) in clientes.items():
        if cid != remetente_id:
            try:
                conn.send(mensagem.encode('utf-8'))  # Envia mensagem para o cliente
            except:
                pass  # Se houver erro (ex: cliente caiu), ignora

# Função que envia uma mensagem para um cliente ESPECÍFICO (mensagem privada)
def enviar_para_cliente(destino_id, mensagem):
    if destino_id in clientes:
        conn, _ = clientes[destino_id]
        try:
            conn.send(mensagem.encode('utf-8'))  # Envia somente para o destino
        except:
            pass  # Se não conseguir, ignora

# Função que gerencia o comportamento de um cliente individual
def handle_cliente(conn, addr):
    try:
        # Solicita o ID do cliente
        conn.send("Digite seu ID: ".encode())
        id_cliente = int(conn.recv(1024).decode())

        # Solicita o NOME do cliente
        conn.send("Digite seu nome: ".encode())
        nome = conn.recv(1024).decode()

        # Salva o nome no histórico de usuários
        registro_nomes[id_cliente] = nome
        # Adiciona o cliente à lista de online
        clientes[id_cliente] = (conn, nome)

        print(f"[+] {nome} (ID {id_cliente}) conectado.")

        # Envia a lista de usuários (quem está online e offline) para o cliente que acabou de entrar
        status_msg = "\n--- STATUS DOS USUÁRIOS ---\n"
        for cid, nome_reg in registro_nomes.items():
            status = "Online" if cid in clientes else "Offline"
            status_msg += f"{nome_reg} (ID {cid}): {status}\n"
        status_msg += "---------------------------\n"
        conn.send(status_msg.encode())

        # Loop que fica ouvindo mensagens enviadas por esse cliente
        while True:
            msg = conn.recv(1024).decode()

            # Verifica se a mensagem é privada (formato: @ID:mensagem)
            if msg.startswith("@"):
                try:
                    parte = msg.split(":", 1)
                    destino_id = int(parte[0][1:])     # Pega o ID após o @
                    conteudo = parte[1]                # Pega o conteúdo da mensagem
                    enviar_para_cliente(destino_id, f"{nome} (privado): {conteudo}")
                except:
                    # Se algo der errado no formato, avisa o cliente
                    conn.send("Erro no formato da mensagem privada.\n".encode())
            else:
                # Se não for mensagem privada, envia para todos os outros
                broadcast(f"{nome}: {msg}", remetente_id=id_cliente)

    except Exception as e:
        print(f"[!] Cliente ID {id_cliente} desconectou. {e}")
    finally:
        # Remove o cliente da lista de online ao sair
        if id_cliente in clientes:
            del clientes[id_cliente]
            print(f"[-] {nome} (ID {id_cliente}) saiu do chat.")
            broadcast(f"{nome} saiu do chat.", remetente_id=id_cliente)
        conn.close()  # Fecha a conexão com o cliente

# Função principal que inicia o servidor
def main():
    host = '127.0.0.1'    # Endereço IP local (localhost)
    port = 12345          # Porta de escuta (pode ser qualquer uma livre)

    # Cria o socket do servidor (TCP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))  # Liga o socket ao IP e porta
    servidor.listen()            # Começa a escutar conexões

    print(f"Servidor escutando em {host}:{port}")

    # Loop principal: aceita conexões de novos clientes
    while True:
        conn, addr = servidor.accept()  # Aceita a conexão de um cliente
        thread = threading.Thread(target=handle_cliente, args=(conn, addr))
        thread.start()  # Cria uma thread separada para esse cliente

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
