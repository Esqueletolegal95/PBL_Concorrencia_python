import socket
import requests
dados = {}
true = 'Ligado'
false = 'Desligado'

def get_host_ip_address():
    """
    Função para obter o endereço IP do host.
    """
    return socket.gethostbyname(socket.gethostname())

host_ip = get_host_ip_address()
print(host_ip)
def pegar_dados():
    try:
        # Fazendo a requisição GET
        response = requests.get(f'http://{host_ip}:5050/udp_dados')

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON
            return data
        else:
            print('Erro na requisição:', response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")


def mudar_temperatura(novaTemperatura, porta):
    try:
        # Define a URL e os dados a serem enviados
        url = f'http://{host_ip}:5050/mudar_temperatura'
        payload = {'novaTemperatura': novaTemperatura, 'porta': porta}

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



def menu():
    while True:
        print("Escolha uma opção:")
        print("1- Visualizar informações")
        print("2- Ligar/Desligar dispositivo")
        print("3- Mudar Temperatura")
        print("4- Sair do programa")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            visualizar_informacoes()
        elif opcao == '2':
            porta = int(input("Digite a porta do dispositivo a ser Ligado/Desligado: "))
            ligar_desligar_dispositivo('ligar',porta)
        elif opcao == '3':
            porta = int(input("Digite a porta do dispositivo: "))
            temperatura = int(input("Digite a temperatura: "))
            mudar_temperatura(porta, temperatura)
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
        temperatura = porta_info['temperatura']
        ligado = porta_info['ligado']
        # Imprime as informações da porta
        print(f"Informações da Porta {chave}:")
        print(f"Porta: {porta}")
        if ligado == "Ligado":
            print(f"Temperatura: {temperatura}")
        print(f"Ligado: {ligado}")
        print()
    # Lógica para visualizar informações
    print("Visualizando informações...")

def ligar_desligar_dispositivo(ligar_desligar, porta):
    # Lógica para ligar/desligar dispositivo
    try:
        # Define a URL e os dados a serem enviados
        url = f'http://{host_ip}:5050/ligar_desligar'
        payload = {'ligar_desligar': ligar_desligar, 'porta': porta}

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
