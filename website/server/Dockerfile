FROM node:8
WORKDIR ~/github/sport-site/website

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8000

CMD ["npm", "start"]
