<template>
  <div class="space-y-6">
    <!-- Заголовок -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Управление заявками</h1>
    </div>

    <!-- Фильтры -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="form-label">Поиск</label>
          <input v-model="filters.search" type="text" placeholder="Имя, email..." class="form-input">
        </div>
        <div>
          <label class="form-label">Группа</label>
          <select v-model="filters.group" class="form-input">
            <option value="">Все группы</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">
              {{ group.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="form-label">Статус</label>
          <select v-model="filters.status" class="form-input">
            <option value="">Все статусы</option>
            <option value="new">Новые</option>
            <option value="processed">Обработанные</option>
            <option value="rejected">Отклоненные</option>
          </select>
        </div>
        <div>
          <label class="form-label">Сортировка</label>
          <select v-model="filters.ordering" class="form-input">
            <option value="-created_at">По дате подачи</option>
            <option value="name">По имени</option>
            <option value="group">По группе</option>
            <option value="status">По статусу</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Список заявок -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Заявки</h2>
      </div>
      
      <div v-if="loading" class="p-6 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-gray-600">Загрузка...</p>
      </div>
      
      <div v-else-if="applications.length === 0" class="p-6 text-center">
        <p class="text-gray-500">Заявки не найдены</p>
      </div>
      
      <div v-else class="divide-y divide-gray-200">
        <div v-for="application in applications" :key="application.id" class="p-6 hover:bg-gray-50">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-lg font-medium text-gray-900">{{ application.name }}</h3>
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  application.status === 'new' ? 'bg-yellow-100 text-yellow-800' :
                  application.status === 'processed' ? 'bg-green-100 text-green-800' :
                  'bg-red-100 text-red-800'
                ]">
                  {{ getStatusDisplay(application.status) }}
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                  <p><strong>Email:</strong> {{ application.email }}</p>
                  <p v-if="application.phone"><strong>Телефон:</strong> {{ application.phone }}</p>
                  <p><strong>Группа:</strong> {{ application.group.name }}</p>
                </div>
                <div>
                  <p><strong>Дата подачи:</strong> {{ formatDate(application.created_at) }}</p>
                  <p v-if="application.comment"><strong>Комментарий:</strong> {{ application.comment }}</p>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-2 ml-4">
              <select v-model="application.status" @change="changeStatus(application)" 
                      class="form-input text-sm py-1">
                <option value="new">Новая</option>
                <option value="processed">Обработанная</option>
                <option value="rejected">Отклоненная</option>
              </select>
              
              <button @click="deleteApplication(application)" class="btn btn-danger text-sm">
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с деталями заявки -->
    <div v-if="showDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-bold text-gray-900">Детали заявки</h3>
            <button @click="closeDetailsModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <div v-if="selectedApplication" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="form-label">Имя</label>
                <p class="text-gray-900">{{ selectedApplication.name }}</p>
              </div>
              
              <div>
                <label class="form-label">Email</label>
                <p class="text-gray-900">{{ selectedApplication.email }}</p>
              </div>
              
              <div v-if="selectedApplication.phone">
                <label class="form-label">Телефон</label>
                <p class="text-gray-900">{{ selectedApplication.phone }}</p>
              </div>
              
              <div>
                <label class="form-label">Группа</label>
                <p class="text-gray-900">{{ selectedApplication.group.name }}</p>
              </div>
              
              <div>
                <label class="form-label">Статус</label>
                <select v-model="selectedApplication.status" @change="changeStatus(selectedApplication)" 
                        class="form-input">
                  <option value="new">Новая</option>
                  <option value="processed">Обработанная</option>
                  <option value="rejected">Отклоненная</option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Дата подачи</label>
                <p class="text-gray-900">{{ formatDate(selectedApplication.created_at) }}</p>
              </div>
            </div>
            
            <div v-if="selectedApplication.comment">
              <label class="form-label">Комментарий</label>
              <p class="text-gray-900 whitespace-pre-line">{{ selectedApplication.comment }}</p>
            </div>
            
            <div class="pt-4 border-t border-gray-200 flex justify-end">
              <button @click="closeDetailsModal" class="btn btn-secondary">
                Закрыть
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import axios from '../config/axios.js'

export default {
  name: 'Applications',
  setup() {
    const applications = ref([])
    const groups = ref([])
    const loading = ref(false)
    const showDetailsModal = ref(false)
    const selectedApplication = ref(null)
    
    const filters = ref({
      search: '',
      group: '',
      status: '',
      ordering: '-created_at'
    })
    
    const loadApplications = async () => {
      loading.value = true
      try {
        const params = { ...filters.value }
        const response = await axios.get('/api/applications/', { params })
        applications.value = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки заявок:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadGroups = async () => {
      try {
        const response = await axios.get('/api/groups/')
        groups.value = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки групп:', error)
      }
    }
    
    const changeStatus = async (application) => {
      try {
        await axios.post(`/api/applications/${application.id}/change_status/`, {
          status: application.status
        })
        // Обновляем список после изменения статуса
        await loadApplications()
      } catch (error) {
        console.error('Ошибка изменения статуса:', error)
        // Возвращаем предыдущий статус при ошибке
        application.status = application._previousStatus
      }
    }
    
    const deleteApplication = async (application) => {
      if (!confirm(`Вы уверены, что хотите удалить заявку от "${application.name}"?`)) return
      
      try {
        await axios.delete(`/api/applications/${application.id}/`)
        await loadApplications()
      } catch (error) {
        console.error('Ошибка удаления заявки:', error)
      }
    }
    
    const showApplicationDetails = (application) => {
      selectedApplication.value = { ...application }
      showDetailsModal.value = true
    }
    
    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedApplication.value = null
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
      return date.toLocaleDateString('ru-RU') + ' ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    }
    
    // Сохраняем предыдущий статус перед изменением
    watch(applications, (newApplications) => {
      newApplications.forEach(app => {
        if (!app._previousStatus) {
          app._previousStatus = app.status
        }
      })
    }, { deep: true })
    
    // Автоматическая загрузка при изменении фильтров
    watch(filters, () => {
      loadApplications()
    }, { deep: true })
    
    onMounted(() => {
      loadApplications()
      loadGroups()
    })
    
    return {
      applications,
      groups,
      loading,
      showDetailsModal,
      selectedApplication,
      filters,
      changeStatus,
      deleteApplication,
      showApplicationDetails,
      closeDetailsModal,
      getStatusDisplay,
      formatDate
    }
  }
}
</script>
