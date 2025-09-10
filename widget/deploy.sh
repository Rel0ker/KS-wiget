#!/bin/bash

# Скрипт деплоя widget на сервер

echo "🚀 Начинаем деплой widget..."

# Создание директории для деплоя
echo "📁 Создаем директорию для деплоя..."
mkdir -p dist

# Копирование файлов widget
echo "📋 Копируем файлы widget..."
cp widget.js dist/
cp schedule-styles.css dist/
cp index.html dist/
cp demo.html dist/

# Создание минифицированной версии (опционально)
echo "🗜️ Создаем минифицированную версию..."
if command -v uglifyjs &> /dev/null; then
    uglifyjs widget.js -o dist/widget.min.js
    echo "✅ Создана минифицированная версия widget.min.js"
else
    echo "⚠️ uglifyjs не найден, пропускаем минификацию"
fi

# Копирование на сервер
echo "📤 Копируем файлы на сервер..."
scp -r dist/* user@ksdev-re.ru:/var/www/ksdev-re.ru/ || echo "⚠️ Не удалось скопировать файлы. Проверьте SSH доступ."

# Настройка nginx для widget
echo "⚙️ Настройка nginx для widget..."
cat > /etc/nginx/sites-available/ks.dev-re.ru << 'EOF'
server {
    listen 80;
    server_name ks.dev-re.ru www.ks.dev-re.ru ksdev-re.ru www.ksdev-re.ru;
    
    root /var/www/ksdev-re.ru;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Кэширование статических файлов
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # CORS заголовки для widget
    location ~* \.(js|css)$ {
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type";
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
ln -sf /etc/nginx/sites-available/ks.dev-re.ru /etc/nginx/sites-enabled/

# Перезагрузка nginx
echo "🔄 Перезагружаем nginx..."
nginx -t && systemctl reload nginx

echo "✅ Widget успешно развернут!"
echo "🌐 Widget доступен по адресу: https://ks.dev-re.ru"
echo "📖 Демо: https://ks.dev-re.ru/demo.html"
