import axios from 'axios'

// Production API URL
axios.defaults.baseURL = 'https://back.ks.dev-re.ru'

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

export default axios

