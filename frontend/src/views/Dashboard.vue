<template>
  <div class="space-y-6">
    <!-- Заголовок -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-8 text-white">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold mb-2">🌟 Панель управления KS Widget</h1>
          <p class="text-blue-100 text-lg">Добро пожаловать в систему управления группами корейского языка</p>
        </div>
        <div class="hidden md:block">
          <a href="https://ks.dev-re.ru" target="_blank" 
             class="inline-flex items-center px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors shadow-lg">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
            </svg>
            Посмотреть виджет
          </a>
        </div>
      </div>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-white shadow-lg rounded-xl p-6 border-l-4 border-blue-500 hover:shadow-xl transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 mb-1">Всего групп</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalGroups }}</p>
            <p class="text-xs text-gray-500 mt-1">Всего создано групп</p>
          </div>
          <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white shadow-lg rounded-xl p-6 border-l-4 border-green-500 hover:shadow-xl transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 mb-1">Активные группы</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.activeGroups }}</p>
            <p class="text-xs text-gray-500 mt-1">Сейчас проводятся</p>
          </div>
          <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white shadow-lg rounded-xl p-6 border-l-4 border-yellow-500 hover:shadow-xl transition-shadow sm:col-span-2 lg:col-span-1">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 mb-1">Новые заявки</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.newApplications }}</p>
            <p class="text-xs text-gray-500 mt-1">Требуют обработки</p>
          </div>
          <div class="w-16 h-16 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-2xl flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="bg-white shadow-lg rounded-xl p-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <svg class="w-6 h-6 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
        Быстрые действия
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link to="/groups" class="group flex items-center p-6 border-2 border-gray-100 rounded-xl hover:border-blue-300 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-blue-50">
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">Создать группу</h3>
            <p class="text-sm text-gray-600">Добавить новую группу для изучения корейского языка</p>
          </div>
        </router-link>

        <router-link to="/applications" class="group flex items-center p-6 border-2 border-gray-100 rounded-xl hover:border-green-300 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-green-50">
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-green-600 transition-colors">Просмотр заявок</h3>
            <p class="text-sm text-gray-600">Управление заявками на участие в группах</p>
          </div>
        </router-link>

        <a href="https://ks.dev-re.ru" target="_blank" 
           class="group flex items-center p-6 border-2 border-gray-100 rounded-xl hover:border-purple-300 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-purple-50">
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">Посмотреть виджет</h3>
            <p class="text-sm text-gray-600">Открыть виджет в новой вкладке</p>
          </div>
        </a>
      </div>
    </div>

    <!-- Последние заявки -->
    <div class="bg-white shadow-lg rounded-xl p-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <svg class="w-6 h-6 mr-3 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        Последние заявки
      </h2>
      <div v-if="recentApplications.length === 0" class="text-center py-12">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
        </div>
        <p class="text-gray-500 text-lg">Нет заявок для отображения</p>
        <p class="text-gray-400 text-sm mt-2">Новые заявки появятся здесь</p>
      </div>
      <div v-else class="space-y-4">
        <div v-for="application in recentApplications" :key="application.id" 
             class="flex items-center justify-between p-6 border-2 border-gray-100 rounded-xl hover:border-blue-200 hover:shadow-md transition-all duration-300 bg-gradient-to-r from-white to-gray-50">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center">
              <span class="text-white font-bold text-lg">{{ application.name.charAt(0).toUpperCase() }}</span>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{{ application.name }}</h3>
              <p class="text-sm text-gray-600">{{ application.email }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ application.group.name }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span :class="[
              'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
              application.status === 'new' ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' :
              application.status === 'processed' ? 'bg-green-100 text-green-800 border border-green-200' :
              'bg-red-100 text-red-800 border border-red-200'
            ]">
              {{ getStatusDisplay(application.status) }}
            </span>
            <span class="text-sm text-gray-500">{{ formatDate(application.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from '../config/axios.js'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      totalGroups: 0,
      activeGroups: 0,
      newApplications: 0
    })
    
    const recentApplications = ref([])
    
    const loadStats = async () => {
      try {
        const [groupsResponse, applicationsResponse] = await Promise.all([
          axios.get('/api/groups/'),
          axios.get('/api/applications/')
        ])
        
        const groups = groupsResponse.data.results || groupsResponse.data
        const applications = applicationsResponse.data.results || applicationsResponse.data
        
        stats.value = {
          totalGroups: groups.length,
          activeGroups: groups.filter(g => g.is_active).length,
          newApplications: applications.filter(a => a.status === 'new').length
        }
        
        recentApplications.value = applications
          .filter(a => a.status === 'new')
          .slice(0, 5)
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    }
    
    const getStatusDisplay = (status) => {
      const statusMap = {
        'new': 'Новая',
        'processed': 'Обработанная',
        'rejected': 'Отклоненная'
      }
      return statusMap[status] || status
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU')
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      stats,
      recentApplications,
      getStatusDisplay,
      formatDate
    }
  }
}
</script>
