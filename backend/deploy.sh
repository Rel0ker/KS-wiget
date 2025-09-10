#!/bin/bash

# Скрипт деплоя backend на сервер

echo "🚀 Начинаем деплой backend..."

# Остановка существующих процессов
echo "⏹️ Останавливаем существующие процессы..."
pkill -f "gunicorn.*ks_widget" || true
pkill -f "python.*manage.py.*runserver" || true

# Активация виртуального окружения
echo "🐍 Активируем виртуальное окружение..."
source venv/bin/activate

# Установка зависимостей
echo "📦 Устанавливаем зависимости..."
pip install -r requirements-production.txt

# Создание директорий
echo "📁 Создаем необходимые директории..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

# Применение миграций
echo "🗄️ Применяем миграции..."
python manage.py migrate --settings=ks_widget.settings_production

# Сбор статических файлов
echo "📄 Собираем статические файлы..."
python manage.py collectstatic --noinput --settings=ks_widget.settings_production

# Создание суперпользователя (если нужно)
echo "👤 Создание суперпользователя (если нужно)..."
python manage.py createsuperuser --settings=ks_widget.settings_production || true

# Запуск с gunicorn
echo "🚀 Запускаем сервер с gunicorn..."
gunicorn --config gunicorn.conf.py ks_widget.wsgi:application --settings=ks_widget.settings_production &

echo "✅ Backend успешно развернут!"
echo "🌐 Сервер доступен по адресу: https://back.ks.dev-re.ru"
echo "📊 Логи: tail -f logs/gunicorn_access.log"

