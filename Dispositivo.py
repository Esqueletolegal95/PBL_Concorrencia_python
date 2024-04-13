import socket
import random
import time
import json

def get_host_ip_address():
    """
    Função para obter o endereço IP do host.
    """
    return socket.gethostbyname(socket.gethostname())

host_ip = get_host_ip_address()

def enviar_mensagem(temperatura):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                mensagem_dict = {
                    'ip': host_ip,
                    'temperatura': temperatura
                }
                
                mensagem_json = json.dumps(mensagem_dict)
                
                s.sendto(mensagem_json.encode(), ("localhost", 1234))
                
                print(f"Mensagem enviada: {mensagem_json}")
                
                time.sleep(1)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def main():
    try:
        temperatura = random.randint(0, 34)
        enviar_mensagem(temperatura)
    except Exception as e:
        print(f"Erro no main: {e}")

if __name__ == "__main__":
    main()