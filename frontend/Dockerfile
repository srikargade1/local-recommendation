# Stage 1: Build the React app
FROM node:18 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine AS production

# Copy the CRA build to Nginx's default public folder
COPY --from=build /app/build /usr/share/nginx/html

# Optional: Remove default nginx config and replace with your own
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

