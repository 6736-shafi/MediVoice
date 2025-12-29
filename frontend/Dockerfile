# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
# We need package.json AND package-lock.json for clean install
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/server.js ./

# Install production dependencies (including express, since we added it)
RUN npm install --omit=dev

ENV PORT=8080
CMD ["node", "server.js"]
