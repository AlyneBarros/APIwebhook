# Use a imagem base do Python
FROM python:3

# Define o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY app.py .
COPY dados.db .
COPY src/app.py .


# Instale as dependências do aplicativo
RUN pip install flask flasgger

# Exponha a porta em que o seu aplicativo está escutando
EXPOSE 5001

# Execute o arquivo python quando o container iniciar
CMD [ "python", "./app.py" ]
