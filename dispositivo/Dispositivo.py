import socket
import random
import json
import time
import threading

# Gera uma temperatura aleatória entre 0 e 34 graus Celsius
temperatura = random.randint(0, 34)
# Define o estado inicial como ligado
ligado = True
# Variável global para armazenar a porta atual
current_port = 0

# Função para modificar a temperatura
def modificar_temperatura(nova_temperatura):
    global temperatura
    temperatura = nova_temperatura

# Função para obter o endereço IP do host
def get_host_ip_address():
    return socket.gethostbyname(socket.gethostname())

# Obtém o endereço IP do host
host_ip = get_host_ip_address()

# Função para ligar/desligar o dispositivo
def liga_desliga():
    global ligado
    ligado = not ligado

# Função para encontrar uma porta livre
def encontrar_porta_livre(initial_port):
    global current_port
    current_port = initial_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host_ip, current_port))
                return current_port
        except OSError:
            current_port += 1

# Função para enviar mensagem via UDP
def enviar_mensagem_udp():
    global temperatura
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                # Cria um dicionário com os dados a serem enviados
                mensagem_dict = {
                    'ip': host_ip,
                    'porta': current_port,
                    'temperatura': temperatura,
                    'ligado': ligado
                }
                # Converte o dicionário em JSON
                mensagem_json = json.dumps(mensagem_dict)
                # Envia os dados via UDP para o endereço e porta especificados
                s.sendto(mensagem_json.encode(), ("172.17.0.4", 1234))
                # Aguarda um segundo antes de enviar a próxima mensagem
                time.sleep(1)
    except Exception as e:
        print(f"Erro ao enviar mensagem UDP: {e}")

# Função para receber mensagens via TCP
def receber_mensagem_tcp():
    global temperatura
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Encontra uma porta livre para escutar as conexões TCP
            porta_tcp = encontrar_porta_livre(1237)
            s.bind(("0.0.0.0", porta_tcp))
            s.listen(1)  # Aceita apenas uma conexão por vez
            print(f"Aguardando conexão TCP em {host_ip}:{porta_tcp}...")
            conn, addr = s.accept()  # Aceita uma conexão
            print(f"Conexão estabelecida com {addr}")
            while True:
                data = conn.recv(1024)  # Recebe dados do cliente
                if not data:
                    break
                mensagem = json.loads(data.decode())  # Decodifica a mensagem JSON
                if "Temperatura" in mensagem:
                    temperatura = mensagem["Temperatura"]
                    print(temperatura)
                elif "ligar_desligar" in mensagem:
                    liga_desliga()
                    print(ligado)
                print(f"Mensagem TCP recebida: {mensagem}")
    except Exception as e:
        print(f"Erro ao receber mensagem TCP: {e}")

# Função para iniciar o servidor UDP em uma thread separada
def servidor_udp():
    enviar_mensagem_udp()

# Função do menu
def menu():
    while True:
        print("\nMenu:")
        print("1. Mudar temperatura")
        print("2. Ligado/Desligado")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nova_temperatura = int(input("Digite a nova temperatura: "))
            modificar_temperatura(nova_temperatura)
        elif opcao == "2":
            liga_desliga()
            print("Dispositivo ligado" if ligado else "Dispositivo desligado")
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")

# Função principal
def main():
    try:
        # Inicia duas threads para executar o servidor UDP e TCP simultaneamente
        udp_thread = threading.Thread(target=servidor_udp)
        tcp_thread = threading.Thread(target=receber_mensagem_tcp)
        udp_thread.start()
        tcp_thread.start()
        
        # Inicia o menu em uma thread separada
        menu_thread = threading.Thread(target=menu)
        menu_thread.start()
        
        # Aguarda a conclusão do menu
        menu_thread.join()
    except Exception as e:
        print(f"Erro no main: {e}")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
