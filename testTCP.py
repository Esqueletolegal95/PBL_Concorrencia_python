import socket
import threading

# Função para tratar conexões TCP dos clientes
def handle_client(client_socket, dados_recebidos):
    while True:
        # Recebe os dados do cliente
        dados = client_socket.recv(1024).decode()

        if not dados:
            break
        
        # Adiciona os dados recebidos à lista de dados
        dados_recebidos.append(dados)
        
        # Exibe os dados recebidos
        print("Dados recebidos:", dados)

    # Fecha o socket do cliente
    client_socket.close()

# Função principal
def main():
    # Inicializa o servidor TCP
    tcp_host = '192.168.0.105'
    tcp_port = 9999
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((tcp_host, tcp_port))
    tcp_socket.listen(5)

    print("Servidor TCP iniciado. Aguardando conexões...")

    # Lista para armazenar os dados recebidos
    dados_recebidos = []

    while True:
        # Aceita a conexão de um cliente
        client_socket, addr = tcp_socket.accept()
        print("Conexão estabelecida com", addr)

        # Inicia uma nova thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, dados_recebidos))
        client_handler.start()

if __name__ == '__main__':
    main()