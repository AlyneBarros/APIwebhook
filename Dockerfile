# Use uma imagem base do Python
FROM python:3

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie tudo da pasta raiz do projeto para a pasta raiz do container
COPY . .

# Execute o arquivo python quando o container iniciar
CMD [ "python", "./app.py" ]
