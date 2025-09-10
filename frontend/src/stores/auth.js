import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '../config/axios.production.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  
  // Настройка axios
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }
  
  const isAuthenticated = computed(() => !!token.value)
  
  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/token/', credentials)
      const { access, refresh } = response.data
      
      token.value = access
      localStorage.setItem('token', access)
      localStorage.setItem('refresh_token', refresh)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      // Получаем информацию о пользователе
      await fetchUser()
      
      return { success: true }
    } catch (error) {
      console.error('Ошибка входа:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Ошибка входа' 
      }
    }
  }
  
  const fetchUser = async () => {
    try {
      const response = await axios.get('/api/user/')
      user.value = response.data
    } catch (error) {
      console.error('Ошибка получения пользователя:', error)
      logout()
    }
  }
  
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    delete axios.defaults.headers.common['Authorization']
  }
  
  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        throw new Error('Нет refresh token')
      }
      
      const response = await axios.post('/api/token/refresh/', {
        refresh: refresh
      })
      
      const { access } = response.data
      token.value = access
      localStorage.setItem('token', access)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      return true
    } catch (error) {
      console.error('Ошибка обновления токена:', error)
      logout()
      return false
    }
  }
  
  // Проверяем токен при инициализации
  if (token.value) {
    fetchUser()
  }
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    fetchUser,
    refreshToken
  }
})
