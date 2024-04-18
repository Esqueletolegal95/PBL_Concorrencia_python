import socket
import threading
import json

udp_dados = {}
tcp_dados = {}

def handle_client_udp(client_address, client_port, data):
    try:
        mensagem_cliente = data.decode()
        print(f"Mensagem UDP do cliente {client_address}:{client_port}: {mensagem_cliente}")
        udp_dados[client_port] = mensagem_cliente
        print(udp_dados)
    except Exception as e:
        print(e)

def handle_client_tcp(client_socket, client_address):
    try:
        data = client_socket.recv(1024)
        mensagem_cliente = data.decode('utf-8')
        print(f"Mensagem TCP do cliente {client_address[0]}:{client_address[1]}: {mensagem_cliente}")
        tcp_dados[client_address[1]] = mensagem_cliente
        client_socket.close()

    except Exception as e:
        print(e)

def iniciar_udp(server_socket):
    try:
        print("Servidor UDP iniciado. Aguardando mensagens...")
        while True:
            data, client_address = server_socket.recvfrom(1024)
            client_ip, client_port = client_address
            client_thread = threading.Thread(target=handle_client_udp, args=(client_ip, client_port, data))
            client_thread.start()
            
    except Exception as e:
        print(e)

def iniciar_tcp(server_socket):
    try:
        print("Servidor TCP iniciado. Aguardando conexões...")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_tcp, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(e)

def enviar_via_tcp(dados_json):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))
            mensagem_json = json.dumps(dados_json)
            s.sendall(mensagem_json.encode('utf-8'))
            print("Mensagem enviada via TCP")
        
    except Exception as e:
        print(f"Erro ao enviar mensagem via TCP: {e}")


def main():
    try:
        # Iniciar servidor UDP
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server_socket.bind(('localhost', 1234))

        # Iniciar servidor TCP
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.bind(('0.0.0.0', 5000))
        tcp_server_socket.listen(5)  # Permitir até 5 conexões pendentes

        # Threads para os servidores UDP e TCP
        udp_thread = threading.Thread(target=iniciar_udp, args=(udp_server_socket,))
        tcp_thread = threading.Thread(target=iniciar_tcp, args=(tcp_server_socket,))
        

        udp_thread.start()
        tcp_thread.start()
        enviar_via_tcp({"temperatura": 43})

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
