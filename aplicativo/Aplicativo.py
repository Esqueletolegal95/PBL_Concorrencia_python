import socket
import requests
dados = {}
true = 'Ligado'
false = 'Desligado'
ip_dispositivos = '172.17.0.' #ultimo número será dito pelo usuário


def get_host_ip_address():
    """
    Função para obter o endereço IP do host.
    """
    return socket.gethostbyname(socket.gethostname())

ip_broker= '172.16.103.13'

def pegar_dados():
    try:
        # Fazendo a requisição GET1
        response = requests.get(f'http://{ip_broker}:5050/udp_dados')

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON
            return data
        else:
            print('Erro na requisição:', response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")


def mudar_temperatura(novaTemperatura, ip):
    try:
        # Define a URL e os dados a serem enviados
        url = f'http://{ip_broker}:5050/mudar_temperatura'
        payload = {'novaTemperatura': novaTemperatura,'ip': ip}

        # Enviar requisição POST com os dados em formato JSON
        response = requests.post(url, json=payload)

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte resposta para JSON
            return data
        else:
            print('Erro na requisição:', response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")



def menu():
    while True:
        global dados
        print("Escolha uma opção:")
        print("1- Visualizar informações")
        print("2- Ligar/Desligar dispositivo")
        print("3- Mudar Temperatura")
        print("4- Sair do programa")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            visualizar_informacoes()
        elif opcao == '2':
            ip = ip_dispositivos + (input("Digite a porta UDP do dispositivo a ser Ligado/Desligado: "))
            ligar_desligar_dispositivo('ligar_desligar',ip)
        elif opcao == '3':
            ip = ip_dispositivos + (input("Digite a porta do dispositivo: "))
            temperatura = int(input("Digite a temperatura: "))
            mudar_temperatura(temperatura, ip)
        elif opcao == '4':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def visualizar_informacoes():
    global dados
    dados = pegar_dados()
    print (dados)
    for chave, valor_json in dados.items():
        # Converte a string JSON em um dicionário Python
        porta_info = eval(valor_json)
        # Extrai as informações da porta
        porta = porta_info['porta']
        ip = porta_info['ip']
        temperatura = porta_info['temperatura']
        ligado = porta_info['ligado']
        # Imprime as informações da porta
        print(f"Informações do ip {ip}:")
        partes = ip.split(".")
        id = partes[-1]
        print(f"Id do dispositivo: {id}")
        print(f"Porta: {porta}")
        if ligado == "Ligado":
            print(f"Temperatura: {temperatura}")
        print(f"Ligado: {ligado}")
        print()
    # Lógica para visualizar informações
    print("Visualizando informações...")

def ligar_desligar_dispositivo(ligar_desligar, ip):
    # Lógica para ligar/desligar dispositivo
    try:
        # Define a URL e os dados a serem enviados
        url = f'http://{ip_broker}:5050/ligar_desligar'
        payload = {'ligar_desligar': ligar_desligar,  'ip': ip}

        # Enviar requisição POST com os dados em formato JSON
        response = requests.post(url, json=payload)

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte resposta para JSON
            print(data)
            return data
        else:
            print('Erro na requisição:', response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")






def main():
    menu()

if __name__ == "__main__":
    main()
