FROM node:16-alpine
ARG GATSBY_API_URL=$GATSBY_API_URL
WORKDIR /app
COPY ./package.json .
RUN apk add --no-cache --update python3 make g++
RUN npm install
COPY ./src/ ./src
COPY ./gatsby-config.ts .
COPY ./tsconfig.json .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "serve"]
