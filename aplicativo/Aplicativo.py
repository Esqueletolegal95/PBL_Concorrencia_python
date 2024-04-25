import requests


def pegar_dados():
    try:
        # Fazendo a requisição GET
        response = requests.get('http://192.168.0.105:5000/udp_dados')

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON
            print(data)
            return data
        else:
            print('Erro na requisição:', response.status_code)
            
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")


def mudar_temperatura(novaTemperatura, porta):
    try:
        # Define a URL e os dados a serem enviados
        url = 'http://192.168.0.105:5000/mudar_temperatura'
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
        

# Chamar a função com os valores desejados
mudar_temperatura(0, 1235)