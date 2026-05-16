# frontend/Dockerfile
FROM node:20-slim
 
WORKDIR /app
 
# Copy package files first.
COPY package.json package-lock.json ./
RUN npm ci
 
COPY . .
 
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
