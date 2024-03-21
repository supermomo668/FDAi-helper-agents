# Stage 1: Building the code
FROM node:21.6.2-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm install -g npm@10.2.4
RUN npm install --save-exact --save-dev typescript @types/react @types/node && npm run build

# Stage 2: Running the application
FROM builder as nextjs-app

# Create a non-root user and set permissions
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

WORKDIR /app
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/package.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

# Environment variables should be passed at runtime for security
# COPY --from=builder /app/.env* ./
USER nextjs

CMD ["npm", "run", "dev"]
