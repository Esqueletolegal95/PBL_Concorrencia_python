import socket
import threading
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

udp_dados = {}  # Dicionário para armazenar dados recebidos via UDP
tcp_dados = {}  # Dicionário para armazenar dados recebidos via TCP

# Função para lidar com dados recebidos via UDP
def handle_client_udp(client_address, client_port, data):
    try:
        mensagem_cliente = data.decode()
        print(f"Mensagem UDP do cliente {client_address}:{client_port}: {mensagem_cliente}")
        udp_dados[client_port] = mensagem_cliente  # Armazenar dados no dicionário
    except Exception as e:
        print(e)

# Função para lidar com dados recebidos via TCP
def handle_client_tcp(client_socket, client_address):
    try:
        data = client_socket.recv(1024)
        mensagem_cliente = data.decode('utf-8')
        print(f"Mensagem TCP do cliente {client_address[0]}:{client_address[1]}: {mensagem_cliente}")
        tcp_dados[client_address[1]] = mensagem_cliente  # Armazenar dados no dicionário
        client_socket.close()  # Fechar o socket após receber os dados
    except Exception as e:
        print(e)

# Rota para obter os dados recebidos via UDP
@app.route('/udp_dados', methods=['GET'])
def get_udp_dados():
    return jsonify(udp_dados)

# Rota para alterar a temperatura
@app.route('/mudar_temperatura', methods=['POST'])
def mudar_temperatura():
    # Receber dados da requisição POST
    data = request.json
    novaTemperatura = data.get('novaTemperatura')
    ip = data.get('ip')
    enviar_via_tcp({"Temperatura":novaTemperatura}, ip)  # Enviar os dados via TCP
    # Retornar uma resposta
    resposta = {"status": "Temperatura alterada com sucesso", "novaTemperatura": novaTemperatura, "ip": ip}
    return jsonify(resposta)

# Rota para ligar ou desligar dispositivos
@app.route('/ligar_desligar', methods=['POST'])
def ligar_desligar():
    # Receber dados da requisição POST
    data = request.json
    ligar_desligar = data.get('ligar_desligar')
    ip = data.get('ip')
    enviar_via_tcp({"ligar_desligar":ligar_desligar}, ip)  # Enviar os dados via TCP
    # Retornar uma resposta
    resposta = {"ligar_desligar": ligar_desligar, "ip": ip}
    return jsonify(resposta)

# Rota para obter os dados recebidos via TCP
@app.route('/tcp_dados', methods=['GET'])
def get_tcp_dados():
    return jsonify(tcp_dados)

# Função para iniciar o servidor UDP
def iniciar_udp(server_socket):
    try:
        print("Servidor UDP iniciado. Aguardando mensagens...")
        while True:
            data, client_address = server_socket.recvfrom(1024)
            client_ip, client_port = client_address
            # Iniciar uma nova thread para lidar com cada cliente UDP
            client_thread = threading.Thread(target=handle_client_udp, args=(client_ip, client_port, data))
            client_thread.start()
    except Exception as e:
        print(e)

# Função para iniciar o servidor TCP
def iniciar_tcp(server_socket):
    try:
        print("Servidor TCP iniciado. Aguardando conexões...")
        while True:
            client_socket, client_address = server_socket.accept()
            # Iniciar uma nova thread para lidar com cada cliente TCP
            client_thread = threading.Thread(target=handle_client_tcp, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(e)

# Função para enviar dados via TCP
def enviar_via_tcp(dados_json, ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 1237))
            mensagem_json = json.dumps(dados_json)
            s.sendall(mensagem_json.encode('utf-8'))
            print("Mensagem enviada via TCP")
    except Exception as e:
        print(dados_json)
        print(f"Erro ao enviar mensagem via TCP: {e}")

if __name__ == "__main__":
    # Iniciar o servidor UDP
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('0.0.0.0', 1234))

    # Iniciar o servidor TCP
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('0.0.0.0', 1235))
    tcp_server_socket.listen(5)

    # Iniciar threads para os servidores UDP e TCP
    udp_thread = threading.Thread(target=iniciar_udp, args=(udp_server_socket,))
    tcp_thread = threading.Thread(target=iniciar_tcp, args=(tcp_server_socket,))
    
    udp_thread.start()  # Iniciar thread do servidor UDP
    tcp_thread.start()  # Iniciar thread do servidor TCP

    # Iniciar o aplicativo Flask para lidar com requisições HTTP
    app.run(host='0.0.0.0', port=5050)
