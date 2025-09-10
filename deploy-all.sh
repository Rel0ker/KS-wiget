#!/bin/bash

# Общий скрипт деплоя всей системы

echo "🚀 Начинаем полный деплой системы KS Widget..."

# Проверка наличия необходимых директорий
if [ ! -d "backend" ] || [ ! -d "frontend" ] || [ ! -d "widget" ]; then
    echo "❌ Ошибка: Не найдены необходимые директории (backend, frontend, widget)"
    exit 1
fi

# Деплой backend
echo "🔧 Деплой backend..."
cd backend
./deploy.sh
if [ $? -ne 0 ]; then
    echo "❌ Ошибка при деплое backend"
    exit 1
fi
cd ..

# Деплой frontend
echo "🎨 Деплой frontend..."
cd frontend
./deploy.sh
if [ $? -ne 0 ]; then
    echo "❌ Ошибка при деплое frontend"
    exit 1
fi
cd ..

# Деплой widget
echo "📱 Деплой widget..."
cd widget
./deploy.sh
if [ $? -ne 0 ]; then
    echo "❌ Ошибка при деплое widget"
    exit 1
fi
cd ..

echo "✅ Полный деплой завершен успешно!"
echo ""
echo "🌐 Доступные адреса:"
echo "   Backend API:  https://back.ks.dev-re.ru"
echo "   Frontend:     https://front.ks.dev-re.ru"
echo "   Widget:       https://ks.dev-re.ru"
echo ""
echo "📊 Мониторинг:"
echo "   Backend logs: tail -f backend/logs/gunicorn_access.log"
echo "   Nginx logs:   tail -f /var/log/nginx/access.log"
echo ""
echo "🔧 Полезные команды:"
echo "   Перезапуск backend: cd backend && ./deploy.sh"
echo "   Перезапуск frontend: cd frontend && ./deploy.sh"
echo "   Перезапуск widget: cd widget && ./deploy.sh"
