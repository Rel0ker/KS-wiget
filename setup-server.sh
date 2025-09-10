#!/bin/bash

# Скрипт настройки сервера для KS Widget

echo "🚀 Начинаем настройку сервера..."

# Обновление системы
echo "📦 Обновляем систему..."
apt update && apt upgrade -y

# Установка зависимостей
echo "🔧 Устанавливаем зависимости..."
apt install -y nginx nodejs npm postgresql postgresql-contrib python3-pip python3-venv python3-dev build-essential

# Запуск PostgreSQL
echo "🗄️ Настраиваем PostgreSQL..."
systemctl start postgresql
systemctl enable postgresql

# Создание базы данных
echo "📊 Создаем базу данных..."
sudo -u postgres psql -c "CREATE DATABASE ks_widget;"
sudo -u postgres psql -c "CREATE USER ks_widget WITH PASSWORD 'ks_widget_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ks_widget TO ks_widget;"

# Создание директорий
echo "📁 Создаем директории..."
mkdir -p /var/www/back.ks.dev-re.ru
mkdir -p /var/www/front.ks.dev-re.ru
mkdir -p /var/www/ks.dev-re.ru
mkdir -p /var/log/ks-widget

# Настройка прав доступа
echo "🔐 Настраиваем права доступа..."
chown -R www-data:www-data /var/www/
chmod -R 755 /var/www/

# Запуск nginx
echo "🌐 Настраиваем nginx..."
systemctl start nginx
systemctl enable nginx

echo "✅ Настройка сервера завершена!"
echo "🌐 Nginx: systemctl status nginx"
echo "🗄️ PostgreSQL: systemctl status postgresql"



