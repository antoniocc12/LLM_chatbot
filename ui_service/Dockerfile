FROM node:21.6.2
RUN apt update

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY ./ .

CMD ["npm", "run", "serve"]