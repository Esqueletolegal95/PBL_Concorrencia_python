## Como executar a aplicação:
 Para executar os dispositivos e o servidor é necessário abrir o terminal até o diretório onde estão os arquivos ```DOCKERFILE``` tanto do server quanto para o cliente e executar os passos abaixo:
 1. **Criar Containers Para Servidor**

    ```bash
    docker build -t server .
    ```

2. **Executar o Container (Configurando a Porta)**

    ```bash
    docker run -p 1234:1234 server
    ```

3. **Executar no Modo Interativo**

    ```bash
    docker run -it server
    ```
 4. **Criar Containers Para Dispositivo**

    ```bash
    docker build -t dispositivo .
    ```

5. **Executar o Container (Configurando a Porta)**

    ```bash
    docker run -p 1234:1234 dispositivo
    ```

6. **Executar no Modo Interativo**

    ```bash
    docker run -it server
    ```
