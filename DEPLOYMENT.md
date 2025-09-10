# 🚀 Инструкция по деплою KS Widget

## 📋 Обзор системы

Система состоит из трех компонентов:
- **Backend** (`back.ks.dev-re.ru`) - Django API
- **Frontend** (`front.ks.dev-re.ru`) - Vue.js админка
- **Widget** (`ksdev-re.ru`) - Виджет расписания

## 🛠️ Требования к серверу

### Backend сервер
- Ubuntu 20.04+ / CentOS 8+
- Python 3.9+
- PostgreSQL 12+
- Nginx
- SSL сертификат

### Frontend сервер
- Ubuntu 20.04+ / CentOS 8+
- Node.js 16+
- Nginx
- SSL сертификат

### Widget сервер
- Ubuntu 20.04+ / CentOS 8+
- Nginx
- SSL сертификат

## 🔧 Подготовка сервера

### 1. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### 2. Настройка PostgreSQL

```bash
# Создание базы данных
sudo -u postgres psql
CREATE DATABASE ks_widget;
CREATE USER ks_widget WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE ks_widget TO ks_widget;
\q
```

### 3. Настройка Nginx

```bash
# Создание директорий
sudo mkdir -p /var/www/back.ks.dev-re.ru
sudo mkdir -p /var/www/front.ks.dev-re.ru
sudo mkdir -p /var/www/ksdev-re.ru

# Настройка прав доступа
sudo chown -R www-data:www-data /var/www/
sudo chmod -R 755 /var/www/
```

## 📦 Деплой

### Автоматический деплой (рекомендуется)

```bash
# Клонирование репозитория
git clone <repository-url>
cd KS-wiget

# Запуск полного деплоя
./deploy-all.sh
```

### Ручной деплой

#### 1. Backend

```bash
cd backend

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements-production.txt

# Настройка переменных окружения
cp env.production.example .env
# Отредактируйте .env файл с вашими настройками

# Применение миграций
python manage.py migrate --settings=ks_widget.settings_production

# Создание суперпользователя
python manage.py createsuperuser --settings=ks_widget.settings_production

# Сбор статических файлов
python manage.py collectstatic --noinput --settings=ks_widget.settings_production

# Запуск с gunicorn
gunicorn --config gunicorn.conf.py ks_widget.wsgi:application --settings=ks_widget.settings_production
```

#### 2. Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Сборка для продакшена
npm run build

# Копирование файлов
sudo cp -r dist/* /var/www/front.ks.dev-re.ru/
```

#### 3. Widget

```bash
cd widget

# Копирование файлов
sudo cp widget.js /var/www/ksdev-re.ru/
sudo cp schedule-styles.css /var/www/ksdev-re.ru/
sudo cp index.html /var/www/ksdev-re.ru/
sudo cp demo.html /var/www/ksdev-re.ru/
```

## ⚙️ Конфигурация Nginx

### Backend (back.ks.dev-re.ru)

```nginx
server {
    listen 80;
    server_name back.ks.dev-re.ru;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

### Frontend (front.ks.dev-re.ru)

```nginx
server {
    listen 80;
    server_name front.ks.dev-re.ru;
    
    root /var/www/front.ks.dev-re.ru;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Widget (ksdev-re.ru)

```nginx
server {
    listen 80;
    server_name ksdev-re.ru www.ksdev-re.ru;
    
    root /var/www/ksdev-re.ru;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(js|css)$ {
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type";
    }
}
```

## 🔒 SSL сертификаты

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение сертификатов
sudo certbot --nginx -d back.ks.dev-re.ru
sudo certbot --nginx -d front.ks.dev-re.ru
sudo certbot --nginx -d ksdev-re.ru
sudo certbot --nginx -d www.ksdev-re.ru

# Автообновление
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Мониторинг

### Логи

```bash
# Backend логи
tail -f backend/logs/gunicorn_access.log
tail -f backend/logs/gunicorn_error.log

# Nginx логи
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Статус сервисов

```bash
# Проверка статуса gunicorn
ps aux | grep gunicorn

# Проверка статуса nginx
sudo systemctl status nginx

# Перезапуск сервисов
sudo systemctl restart nginx
```

## 🔄 Обновление

```bash
# Обновление кода
git pull origin main

# Перезапуск всех сервисов
./deploy-all.sh
```

## 🆘 Устранение неполадок

### Backend не запускается
1. Проверьте логи: `tail -f backend/logs/gunicorn_error.log`
2. Проверьте настройки базы данных в `.env`
3. Убедитесь, что порт 8000 свободен

### Frontend не загружается
1. Проверьте nginx конфигурацию: `sudo nginx -t`
2. Убедитесь, что файлы скопированы в `/var/www/front.ks.dev-re.ru/`
3. Проверьте права доступа: `sudo chown -R www-data:www-data /var/www/`

### Widget не работает
1. Проверьте CORS настройки в backend
2. Убедитесь, что API доступен по `https://back.ks.dev-re.ru`
3. Проверьте консоль браузера на ошибки

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи сервисов
2. Убедитесь в правильности конфигурации
3. Проверьте доступность всех доменов
4. Обратитесь к разработчику

