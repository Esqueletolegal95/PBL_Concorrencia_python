import socket
import random
import json
import time
import threading

temperatura = random.randint(0, 34)
ligado = True

def modificarTemperatura(novaTemperatura):
    return novaTemperatura

def get_host_ip_address():
    """
    Função para obter o endereço IP do host.
    """
    return socket.gethostbyname(socket.gethostname())

host_ip = get_host_ip_address()

def liga_desliga():
    global ligado
    if ligado:
        ligado = False
    else:
        ligado=True

def enviar_mensagem_udp():
    global temperatura
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:

                mensagem_dict = {
                    'ip': host_ip,
                    'porta': 1236,
                    'temperatura': temperatura,
                    'ligado':ligado
                }

                mensagem_json = json.dumps(mensagem_dict)
                
                s.sendto(mensagem_json.encode(), ("localhost", 1234))  # Enviar via UDP

                
                mensagem_json = json.dumps(mensagem_dict)
                
                s.sendto(mensagem_json.encode(), ("localhost", 1234))  # Enviar via UDP

                
                time.sleep(1)
    except Exception as e:
        print(f"Erro ao enviar mensagem UDP: {e}")
    

def receber_mensagem_tcp():
    global temperatura
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 1236))
            s.listen(1)  # Aceitar apenas uma conexão por vez

            print(f"Aguardando conexão TCP em {host_ip}:5000...")
            conn, addr = s.accept()  # Aceitar conexão
            print(f"Conexão estabelecida com {addr}")

            while True:
                data = conn.recv(1024)  # Receber dados do cliente
                if not data:
                    break
                mensagem = json.loads(data.decode())  # Decodificar a mensagem JSON
                if "Temperatura" in mensagem:
                    temperatura = mensagem["Temperatura"]
                    print(temperatura)
                elif "ligar_desligar" in mensagem:
                    liga_desliga() 
                    print(ligado)
                print(f"Mensagem TCP recebida: {mensagem}")
                
    except Exception as e:
        print(f"Erro ao receber mensagem TCP: {e}")

def servidor_udp():
    enviar_mensagem_udp()

def main():
    try:
        udp_thread = threading.Thread(target=servidor_udp)
        tcp_thread = threading.Thread(target=receber_mensagem_tcp)
        
        udp_thread.start()
        tcp_thread.start()

        # Execução principal aqui, se necessário
        input("Pressione Enter para encerrar...\n")
    except Exception as e:
        print(f"Erro no main: {e}")

if __name__ == "__main__":
    main()