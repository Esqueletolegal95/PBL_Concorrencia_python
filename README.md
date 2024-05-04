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
