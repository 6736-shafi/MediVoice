FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build with backend URL

RUN npm run build

# Install express for the production server
RUN npm install express

# Start the server
CMD ["node", "server.js"]
