#!/bin/bash

# Скрипт деплоя frontend на сервер

echo "🚀 Начинаем деплой frontend..."

# Установка зависимостей
echo "📦 Устанавливаем зависимости..."
npm install

# Сборка для продакшена
echo "🔨 Собираем проект для продакшена..."
npm run build

# Создание директории для деплоя
echo "📁 Создаем директорию для деплоя..."
mkdir -p dist

# Копирование файлов
echo "📋 Копируем файлы..."
cp -r dist/* /var/www/front.ks.dev-re.ru/ || echo "⚠️ Не удалось скопировать файлы. Проверьте права доступа."

# Настройка nginx (если нужно)
echo "⚙️ Настройка nginx..."
cat > /etc/nginx/sites-available/front.ks.dev-re.ru << 'EOF'
server {
    listen 80;
    server_name front.ks.dev-re.ru;
    
    root /var/www/front.ks.dev-re.ru;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Кэширование статических файлов
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Gzip сжатие
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
EOF

# Активация сайта
echo "🔗 Активируем сайт..."
ln -sf /etc/nginx/sites-available/front.
ks.dev-re.ru /etc/nginx/sites-enabled/

# Перезагрузка nginx
echo "🔄 Перезагружаем nginx..."
nginx -t && systemctl reload nginx

echo "✅ Frontend успешно развернут!"
echo "🌐 Сайт доступен по адресу: https://front.ks.dev-re.ru"

