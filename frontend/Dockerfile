FROM node:18-alpine

# Definir diretorio de trabalho
WORKDIR /app

# Copiar arquivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar codigo da aplicacao
COPY . .

# Expor porta
EXPOSE 3000

# Comando para executar a aplicacao
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
