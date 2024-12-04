FROM node:14

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 80

CMD ["node", "server.js"]