<template>
  <div class="space-y-6">
    <!-- Заголовок -->
    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold text-gray-900">Панель управления</h1>
      <p class="text-gray-600 mt-2">Добро пожаловать в систему управления группами корейского языка</p>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Всего групп</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalGroups }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Активные группы</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.activeGroups }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Новые заявки</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.newApplications }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <router-link to="/groups" class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-900">Создать группу</h3>
            <p class="text-sm text-gray-500">Добавить новую группу для изучения</p>
          </div>
        </router-link>

        <router-link to="/applications" class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-900">Просмотр заявок</h3>
            <p class="text-sm text-gray-500">Управление заявками на участие</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Последние заявки -->
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Последние заявки</h2>
      <div v-if="recentApplications.length === 0" class="text-center py-8">
        <p class="text-gray-500">Нет заявок для отображения</p>
      </div>
      <div v-else class="space-y-4">
        <div v-for="application in recentApplications" :key="application.id" 
             class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div>
            <h3 class="text-sm font-medium text-gray-900">{{ application.name }}</h3>
            <p class="text-sm text-gray-500">{{ application.email }}</p>
            <p class="text-xs text-gray-400">{{ application.group.name }}</p>
          </div>
          <div class="flex items-center space-x-2">
            <span :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              application.status === 'new' ? 'bg-yellow-100 text-yellow-800' :
              application.status === 'processed' ? 'bg-green-100 text-green-800' :
              'bg-red-100 text-red-800'
            ]">
              {{ getStatusDisplay(application.status) }}
            </span>
            <span class="text-xs text-gray-400">{{ formatDate(application.created_at) }}</span>
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
