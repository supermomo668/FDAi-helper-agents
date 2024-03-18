# Stage 1: Building the code
FROM node:16-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Verify that the next.config.js and public directory are correctly placed and built
RUN ls -la /app

# Stage 2: Running the application
FROM node:16-alpine as nextjs-app

WORKDIR /app
# COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "start"]
