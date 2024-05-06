## Como executar a aplicação:
 Para executar os dispositivos e o servidor é necessário abrir o terminal até o diretório onde estão os arquivos ```DOCKERFILE``` tanto do server quanto para o cliente e executar os passos abaixo:
 1. **Criar Containers Para Servidor**

    ```bash
    docker build -t server .
    ```

2. **Executar o Container (Configurando as Portas)**

    ```bash
     docker run -p 5050:5050 -p 1234:1234/udp -p 1235:1235 server
    ```
 4. **Criar Containers Para Dispositivo**

    ```bash
    docker build -t dispositivo .
    ```

5. **Executar o Container (Configurando a Porta)**

    ```bash
    docker run -p 1237:1237 dispositivo
    ```


Após isso, deverá executar o código `aplicativo.py`, onde verá as opções disponíveis para o gerenciamento dos dispositivos.

## Arquitetura da solução (componentes e mensagens)
A aplicação foi desenvolvida na versão mais recente do Python(3.12.2) e consiste de 3 componentes: uma aplicação, um broker service e um, ou mais, dispositivos. A ordem das mesnsagens trocadas é: O dispositivo envia mensagens para o Broker em loop, a aplicação faz uma requisição ao broker via API REST e por fim o Broker envia mensagem para o dispositivo.
## Protocolo de comunicação entre dispositivo e Broker - camada de transporte
