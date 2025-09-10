FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci --only=production

# Копируем код приложения
COPY . .

# Открываем порт
EXPOSE 3000

# Команда по умолчанию
CMD ["npm", "run", "dev"]
