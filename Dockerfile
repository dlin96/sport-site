FROM node:alpine

WORKDIR /Users/davidlin/github/sport-site/

COPY ./web/package.json .

RUN npm install

COPY . .

EXPOSE 3000
CMD [ "node", "./web/index.js" ]