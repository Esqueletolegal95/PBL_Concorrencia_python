import socket
import threading
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

udp_dados = {}
tcp_dados = {}



def handle_client_udp(client_address, client_port, data):
    try:
        mensagem_cliente = data.decode()
        print(f"Mensagem UDP do cliente {client_address}:{client_port}: {mensagem_cliente}")
        udp_dados[client_port] = mensagem_cliente
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

@app.route('/udp_dados', methods=['GET'])
def get_udp_dados():
    return jsonify(udp_dados)

@app.route('/mudar_temperatura', methods=['POST'])
def mudar_temperatura():
    # Recebendo dados da requisição POST
    data = request.json
    novaTemperatura = data.get('novaTemperatura')
    porta = data.get('porta')
    print(porta)
    enviar_via_tcp({"Temperatura":novaTemperatura}, porta)
    # Exemplo de dados para retornar
    udp_dados = {"status": "Temperatura alterada com sucesso", "novaTemperatura": novaTemperatura, "porta": porta}
    return jsonify(udp_dados)

@app.route('/ligar_desligar', methods=['POST'])
def ligar_desligar():
    # Recebendo dados da requisição POST
    data = request.json
    ligar_desligar = data.get('ligar_desligar')
    porta = data.get('porta')
    
    enviar_via_tcp({"ligar_desligar":ligar_desligar}, porta)
    # Exemplo de dados para retornar
    udp_dados = {"ligar_desligar": ligar_desligar, "porta": porta}
    return jsonify(udp_dados)


@app.route('/tcp_dados', methods=['GET'])
def get_tcp_dados():
    return jsonify(tcp_dados)

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

def enviar_via_tcp(dados_json, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', porta))
            mensagem_json = json.dumps(dados_json)
            s.sendall(mensagem_json.encode('utf-8'))
            print("Mensagem enviada via TCP")
        
    except Exception as e:
        print(dados_json)
        print(f"Erro ao enviar mensagem via TCP: {e}")

if __name__ == "__main__":
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('0.0.0.0', 1234))

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('0.0.0.0', 1235))
    tcp_server_socket.listen(5)

    udp_thread = threading.Thread(target=iniciar_udp, args=(udp_server_socket,))
    tcp_thread = threading.Thread(target=iniciar_tcp, args=(tcp_server_socket,))
    
    udp_thread.start()
    tcp_thread.start()
    app.run(host='0.0.0.0', port=5050)