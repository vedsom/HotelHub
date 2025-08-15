# Stage 1: Build Angular App (optional if already built)
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npx ng build hotel-management --configuration production

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/dist/hotel-management /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
