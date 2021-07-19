FROM node:12-slim

RUN apt-get update && apt-get install -y python python-dev

RUN npm install -g @angular/cli@1.6.6

WORKDIR /code

COPY . .

RUN yarn install

EXPOSE 4200

CMD ["ng", "serve", "--host=0.0.0.0"]
