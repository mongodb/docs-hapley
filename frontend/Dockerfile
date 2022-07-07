FROM node:alpine
WORKDIR /app
COPY ./package.json .
RUN apk add --no-cache --update python3 make g++
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "serve"]
