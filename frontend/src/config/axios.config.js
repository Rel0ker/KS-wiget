import axios from 'axios'

// Определяем окружение
const isProduction = import.meta.env.PROD
const isDevelopment = import.meta.env.DEV

// Базовый URL в зависимости от окружения
let baseURL = 'http://localhost:8000' // development default

if (isProduction) {
  baseURL = 'https://back.ks.dev-re.ru'
} else if (import.meta.env.VITE_API_URL) {
  baseURL = import.meta.env.VITE_API_URL
}

// Настройка базового URL для API
axios.defaults.baseURL = baseURL

// Добавляем заголовки для CORS
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'

// Настройки для CORS
axios.defaults.withCredentials = true

// Перехватчик для обработки ошибок
axios.interceptors.response.use(
  response => response,
  error => {
    console.error('Axios error:', error)
    return Promise.reject(error)
  }
)

// Логирование в development
if (isDevelopment) {
  console.log('API Base URL:', baseURL)
}

export default axios

