FROM node:jod-alpine3.20
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
ENTRYPOINT ["npm", "run", "dev" ]
