#
# Use a imagem base do Python 3.12.3
FROM python:3.12.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo Dispositivo.py para o diretório de trabalho no contêiner
COPY Dispositivo.py .

# Executa o script quando o contêiner for iniciado
CMD ["python", "Dispositivo.py"]

#docker build -t dispositivo .