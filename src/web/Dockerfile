# Build React App
FROM node:15.13-alpine as build-stage
WORKDIR /react
COPY . .
RUN npm install
ENV PATH /react/node_modules/.bin:$PATH
RUN npm run build

# Copy React to Nginx
FROM nginx:latest
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build-stage /react/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]