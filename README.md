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
    docker run -it -p 1237:1237 dispositivo
    ```


Após isso, deverá executar o código `aplicativo.py`, onde verá as opções disponíveis para o gerenciamento dos dispositivos.

## Arquitetura da solução (componentes e mensagens)
A aplicação foi desenvolvida na versão mais recente do Python(3.12.2) e consiste de 3 componentes: uma aplicação, um broker service e um, ou mais, dispositivos. A ordem das mesnsagens trocadas é: O dispositivo envia mensagens para o Broker em loop, a aplicação faz uma requisição ao broker via API REST e por fim o Broker envia mensagem para o dispositivo.
## Protocolo de comunicação entre dispositivo e Broker - camada de transporte
* UDP

Entre o dispositivo e broker é utilizado o protocolo UDP é utilizado para garantir um fluxo constantes de mensagem de forma rápida e eficiente, embora menos segura que o TCP a perda de mensagens se torna irrelevante.

![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/6578091d-e5de-4a64-becf-55f564f68451)


![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/a921684f-d07f-4998-9581-db8374865750)

* TCP

É utilizado também o protocolo TCP para comunicação entre broker e dispositivo para que, assim, mensagens importantes sejam entregeres de forma mais confiável e segura.

![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/9327ffa3-0c66-4ab6-bf58-90d5b141e472)

![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/6c805772-6cd8-4a76-889a-6e41eb97449e)


## Interface da Aplicação (REST)
A solução utiliza o framework Flask para gestão das rotas nos verbos ```GET```e ```POST```, ```PUT```e ```Detele``` não foram utilizado devido à sua irrelevância na gerência do dispositivo.
As rotas são:

![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/88b8ccfb-b372-4908-a906-c471f9618b5c)
![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/ca410621-3f07-4c0f-a82b-d41a16a88cd0)
![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/b8d25b08-03d2-42d4-b03c-b6af6d749ef4)

> [!NOTE]
> Novas rotas podem ser implementadas para tratar outros tipos de dispositivos.

## Formatacao, envio e tratamento de dados
Todos os dados são armazendao em dicionários e convertidos no formado JSON para assim poder ser enviados pelo servidos, pelo dispositivo e pelo aplicativo via API REST nas rotas ```GET```e ```POST```. Dessa forma evitamos que erros envolvendo formatação de dados ocorra.
![image](https://github.com/Esqueletolegal95/PBL_Concorrencia_python/assets/113029820/3ec6dd42-553a-451f-b7be-0ec08f559805)

## Tratamento de conexões simultâeas (threads)
Em relação ao tratamento de conexões simultâneas as threads são utilizadas para tratar o envio e o recebimento de mensagens que foram enviadas em UDP, TCP ou via API REST. Embora nenhum problema em decorrência do uso de threads ou de concorrência foi identificado, vale ressaltar que vários problemas poderão surgir caso uma extrema quantidade de dispositivos ou de aplicações forem conectados causando problemas como:

1 - Condições de corrida: Resultados inconsistentes devido à duas ou mais threads tentando modificar a mesma variável

2 - Deadlock: Uma thread não conseguir terminar a sua execução devido ao uso de um recurso que está sendo utilizada por outra thread

3 - Starvation: Uma fila muito grande de variás threads a serem executadas pode fazer com que uma thread não possa executar

4 - Overhead: Os recursos do sistema podem ser insuficientes para executar um número muito grande de Threads
## Gerenciamento do dispositivo
É possível ligar o dispositivo, mudar a temperatura e visualizar os seus dados remotamente pelo terminal ao executar ```Aplicativo.py``` ou acessar pela interface do dispositivo ao executar ```Dispositivo.py```.
## Desempenho
O sistema utiliza dois mecanismos para melhorar o tempo de resposta para a aplicação, as threads já citadas e o uso de um cache para facilitar a visualização de dados dos dispositivos pela aplicação.

## Confiabilidade da solução
A solução possui tratamento de erros para problemas de conexão
