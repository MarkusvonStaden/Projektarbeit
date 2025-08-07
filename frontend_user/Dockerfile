# Frontend React App
FROM node:18-alpine

WORKDIR /app

# Kopiere package files und installiere dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production=false

# Kopiere den Rest der Anwendung
COPY . .

# Expose Port für Vite Dev Server
EXPOSE 3000

# Für die Entwicklung mit Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]