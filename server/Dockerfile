# Use a imagem base do Python 3.12.3
FROM python:3.12.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos Servidor.py e requirements.txt para o diretório de trabalho no contêiner
COPY Servidor.py .
COPY requirements.txt .

# Instala as dependências do Flask
RUN pip install --no-cache-dir -r requirements.txt

# Executa o script quando o contêiner for iniciado
CMD ["python", "Servidor.py"]
#docker build -t server .