FROM node:9.3-alpine as builder

RUN apk add --no-cache \
  bash \
  python \
  g++ \
  make \
  openssl-dev
WORKDIR /build
ADD package.json ./
RUN npm install --production && \
    cp -r node_modules node_modules_production && \
    npm install
ADD .babelrc .
ADD src ./src
RUN npm run build:production


FROM node:9.3-alpine
WORKDIR /app
COPY --from=builder /build/node_modules_production ./node_modules
COPY --from=builder /build/dist ./dist
ADD package.json ./

CMD ["npm", "run", "start:production"]
