#
# Use a imagem base do Python 3.12.3
FROM python:3.12.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo Servidor.py para o diretório de trabalho no contêiner
COPY Servidor.py .

# Executa o script quando o contêiner for iniciado
CMD ["python", "Servidor.py"]

#docker build -t dispositivo .