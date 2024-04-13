import socket
import threading
import json
dados = {}


def handle_client( client_address, client_port, data):
    try:
        mensagem_cliente = data.decode()
        print(f"Mensagem do cliente {client_address}:{client_port}: {mensagem_cliente}")
        dados_cliente = mensagem_cliente
        dados[client_port] = dados_cliente

        
    except Exception as e:
        print(e)

def iniciar(server_socket):
    try:
        print("Servidor UDP iniciado. Aguardando mensagens...")
        while True:
            data, client_address = server_socket.recvfrom(1024)
            client_ip, client_port = client_address
            client_thread = threading.Thread(target=handle_client, args=(client_ip, client_port, data))
            client_thread.start()
    except Exception as e:
        print(e)

def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', 1234))
        iniciar(server_socket)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
