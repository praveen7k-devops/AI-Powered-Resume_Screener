# Use Node.js to build the React app
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Use nginx to serve the built app
FROM nginx:alpine

# Copy built app from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 3000
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

#docker run -p 3000:80 resume-match-ui
