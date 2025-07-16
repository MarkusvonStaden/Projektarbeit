# Beispiel für ein React App
FROM node:18-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . .

# Für die Entwicklung:
CMD ["npm", "run", "dev"]

# Für Produktion (nachdem du `npm run build` ausgeführt hast):
# CMD ["npm", "run", "build"]
# RUN npm install -g serve
# CMD ["serve", "-s", "build", "-l", "3000"]