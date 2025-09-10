<template>
  <div class="space-y-8 fade-in">
    <!-- Заголовок и кнопка создания -->
    <div class="flex justify-between items-center slide-up">
      <div>
        <h1 class="page-title">Управление группами</h1>
        <p class="text-gray-600 mt-2">Создавайте и управляйте группами корейского языка</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary bounce-in flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Создать группу
      </button>
    </div>

    <!-- Фильтры -->
    <div class="card slide-up">
      <h3 class="section-title">Фильтры и поиск</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <label class="form-label">Поиск</label>
          <input v-model="filters.search" type="text" placeholder="Название группы..." class="form-input">
        </div>
        <div>
          <label class="form-label">Уровень</label>
          <select v-model="filters.level" class="form-input">
            <option value="">Все уровни</option>
            <option v-for="level in levels" v-if="level && level.id" :key="level.id" :value="level.id">
              {{ level.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="form-label">Статус</label>
          <select v-model="filters.status" class="form-input">
            <option value="">Все статусы</option>
            <option value="true">Активные</option>
            <option value="false">Неактивные</option>
          </select>
        </div>
        <div>
          <label class="form-label">Сортировка</label>
          <select v-model="filters.ordering" class="form-input">
            <option value="-created_at">По дате создания</option>
            <option value="name">По названию</option>
            <option value="level__name">По уровню</option>
            <option value="available_spots">По доступным местам</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Список групп -->
    <div class="card slide-up">
      <div class="flex justify-between items-center mb-6">
        <h2 class="section-title mb-0">Группы</h2>
        <div class="flex items-center space-x-2">
          <div class="w-3 h-3 rounded-full animate-pulse" style="background-color: #FF6E23;"></div>
          <span class="text-sm font-medium text-gray-600">{{ groups.length }} групп</span>
        </div>
      </div>
      
      <div v-if="loading" class="p-6 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 mx-auto" style="border-color: #FF6E23;"></div>
        <p class="mt-2 text-gray-600">Загрузка...</p>
      </div>
      
      <div v-else-if="!groups || groups.length === 0" class="p-6 text-center">
        <p class="text-gray-500">Группы не найдены</p>
        <p class="text-xs text-gray-400 mt-2">Debug: groups = {{ JSON.stringify(groups) }}</p>
      </div>
      
      <div v-else class="space-y-4">
                <div v-for="(group, index) in groups" :key="group.id || index" class="group-card fade-in" :style="{ animationDelay: `${index * 0.1}s` }">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-start space-x-4">
                <!-- Цветовой индикатор -->
                <div class="flex-shrink-0 mt-1">
                  <div class="w-3 h-3 rounded-full shadow-sm" :style="{ backgroundColor: group.color || '#3B82F6' }"></div>
                </div>
                
                <!-- Основная информация -->
                <div class="flex-1 min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ group.name }}</h3>
                  
                  <!-- Бейджи статуса -->
                  <div class="flex flex-wrap items-center gap-3 mb-4">
                    <span class="badge badge-blue">
                      {{ group.level?.name || 'Уровень не указан' }}
                    </span>
                    <span class="badge badge-gray">
                      {{ group.available_spots || 0 }}/{{ group.total_capacity || 0 }} мест
                    </span>
                    <span :class="[
                      'badge',
                      group.is_active ? 'badge-green' : 'badge-red'
                    ]">
                      {{ group.is_active ? 'Активна' : 'Неактивна' }}
                    </span>
                  </div>
                  
                  <!-- Описание -->
                  <p v-if="group.description" class="text-sm text-gray-600 mb-3 leading-relaxed">{{ group.description }}</p>
                  
                  <!-- Дополнительная информация -->
                  <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                    <span v-if="group.start_date" class="flex items-center">
                      <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                      Начало: {{ new Date(group.start_date).toLocaleDateString('ru-RU') }}
                    </span>
                    <span v-if="group.schedule" class="flex items-center">
                      <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      {{ group.schedule }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Кнопки управления -->
            <div class="flex items-center space-x-3 ml-4">
              <button @click="editGroup(group)" class="btn btn-secondary text-sm px-4 py-2 flex items-center transition-all duration-200 hover:scale-105 hover:shadow-md">
                <svg class="w-4 h-4 mr-2 transition-transform duration-200 group-hover:rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Редактировать
              </button>
              <button @click="deleteGroup(group)" class="btn btn-danger text-sm px-4 py-2 flex items-center transition-all duration-200 hover:scale-105 hover:shadow-md">
                <svg class="w-4 h-4 mr-2 transition-transform duration-200 group-hover:rotate-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Удалить
              </button>
            </div>
          </div>
        </div>
        </div>
      </div>

    <!-- Модальное окно создания/редактирования -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay">
      <div class="modal-content">
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-bold text-gray-900">
              {{ showEditModal ? 'Редактировать группу' : 'Создать группу' }}
            </h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="form-label">Название группы *</label>
                <input v-model="form.name" type="text" required class="form-input">
              </div>
              
              <div>
                <label class="form-label">Уровень *</label>
                <select v-model="form.level_id" required class="form-input">
                  <option value="">Выберите уровень</option>
                  <option v-for="level in levels" :key="level.id" :value="level.id">
                    {{ level.name }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Общее количество мест *</label>
                <input v-model="form.total_capacity" type="number" min="1" required class="form-input">
              </div>
              
              <div>
                <label class="form-label">Текущее количество участников</label>
                <input v-model="form.current_participants" type="number" min="0" class="form-input">
              </div>
              

              
              <div>
                <label class="form-label">Дата начала</label>
                <input v-model="form.start_date" type="date" class="form-input">
              </div>
              
              <div>
                <label class="form-label">Статус группы</label>
                <div 
                  @click="form.is_active = !form.is_active"
                  :class="[
                    'flex items-center justify-center p-3.5 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-md w-full',
                    form.is_active 
                      ? 'bg-green-50 border-green-300 text-green-800' 
                      : 'bg-red-50 border-red-300 text-red-800'
                  ]"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
                  </svg>
                  <span class="text-sm font-medium">
                    {{ form.is_active ? 'Группа активна' : 'Группа неактивна' }}
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <label class="form-label">Описание</label>
              <textarea v-model="form.description" rows="4" class="form-input"></textarea>
            </div>
            
            <!-- Редактор расписания -->
            <div class="col-span-2">
              <label class="form-label">Расписание занятий</label>
              <div class="border border-gray-300 rounded-xl p-6 bg-gradient-to-br from-gray-50 to-white shadow-sm">
                
                <!-- Шаг 1: Выбор дней недели -->
                <div class="mb-6">
                  <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                    <span class="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold mr-3">1</span>
                    Выберите дни недели
                  </h4>
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div v-for="day in daysOfWeek" :key="day.id" class="relative">
                      <input 
                        :id="`day-${day.id}`"
                        v-model="selectedDays" 
                        :value="day.id" 
                        type="checkbox" 
                        class="sr-only"
                      >
                      <label 
                        :for="`day-${day.id}`" 
                        :class="[
                          'block w-full p-3 text-center rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-md',
                          selectedDays.includes(day.id) 
                            ? 'bg-blue-500 text-white border-blue-500 shadow-lg transform scale-105' 
                            : 'bg-white text-gray-700 border-gray-300 hover:border-blue-300 hover:bg-blue-50'
                        ]"
                      >
                        <div class="font-medium text-sm">{{ getDayName(day.id) }}</div>
                      </label>
                    </div>
                  </div>
                </div>
                
                <!-- Шаг 2: Выбор времени для каждого дня -->
                <div v-if="selectedDays.length > 0" class="mb-6">
                  <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                    <span class="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-bold mr-3">2</span>
                    Выберите время для каждого дня
                  </h4>
                  
                  <div class="space-y-4">
                    <div v-for="dayId in selectedDays" :key="dayId" class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                      <h5 class="font-medium text-gray-800 mb-3 flex items-center">
                        <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        {{ getDayName(dayId) }}
                      </h5>
                      
                      <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                        <div v-for="timeSlot in timeSlots" :key="timeSlot.id" class="relative">
                          <input 
                            :id="`time-${dayId}-${timeSlot.id}`"
                            v-model="scheduleData[dayId]" 
                            :value="timeSlot.id" 
                            type="checkbox" 
                            class="sr-only"
                          >
                          <label 
                            :for="`time-${dayId}-${timeSlot.id}`" 
                            :class="[
                              'block w-full p-2 text-center rounded-md border cursor-pointer transition-all duration-200 text-sm',
                              scheduleData[dayId] && scheduleData[dayId].includes(timeSlot.id)
                                ? 'bg-green-500 text-white border-green-500 shadow-md' 
                                : 'bg-gray-50 text-gray-700 border-gray-300 hover:border-green-300 hover:bg-green-50'
                            ]"
                          >
                            {{ timeSlot.start_time }} - {{ timeSlot.end_time }}
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Предварительный просмотр расписания -->
                <div v-if="hasScheduleData" class="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg">
                  <h4 class="text-sm font-semibold text-blue-800 mb-3 flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Предварительный просмотр расписания
                  </h4>
                  <div class="text-sm text-blue-700 space-y-1">
                    <div v-for="dayId in selectedDays" :key="dayId" class="flex items-start">
                      <span class="font-medium min-w-[80px]">{{ getDayName(dayId) }}:</span>
                      <span v-if="scheduleData[dayId] && scheduleData[dayId].length > 0" class="ml-2">
                        {{ scheduleData[dayId].map(timeId => getTimeSlotText(timeId)).join(', ') }}
                      </span>
                      <span v-else class="ml-2 text-gray-500 italic">время не выбрано</span>
                    </div>
                  </div>
            </div>
            
                <!-- Подсказка -->
                <div v-if="selectedDays.length === 0" class="text-center py-8 text-gray-500">
                  <svg class="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm">Сначала выберите дни недели для занятий</p>
                </div>
              </div>
            </div>
            

            
            <div class="pt-4 border-t border-gray-200 flex justify-end space-x-3">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Отмена
              </button>
              <button type="submit" :disabled="submitting" class="btn btn-primary">
                {{ submitting ? 'Сохранение...' : (showEditModal ? 'Обновить' : 'Создать') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import axios from '../config/axios.js'

export default {
  name: 'Groups',
  setup() {
    const groups = ref([])
    const levels = ref([])
    const daysOfWeek = ref([])
    const timeSlots = ref([])
    const loading = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const submitting = ref(false)
    
    const filters = ref({
      search: '',
      level: '',
      status: '',
      ordering: '-created_at'
    })
    
    const form = ref({
      name: '',
      level_id: '',
      total_capacity: 1,
      current_participants: 0,
      description: '',
      start_date: '',
      schedule: '',
      is_active: true
    })
    
    const selectedDays = ref([])
    const scheduleData = ref({}) // { dayId: [timeSlotIds] }
    
    const loadGroups = async () => {
      loading.value = true
      try {
        const params = { ...filters.value }
        if (params.status === 'true') params.is_active = true
        if (params.status === 'false') params.is_active = false
        delete params.status
        
        const response = await axios.get('/api/groups/', { params })
        const rawGroups = response.data?.results || response.data || []
        
        console.log('Загружены группы:', rawGroups)
        console.log('Параметры запроса:', params)
        
        // Проверяем, что все группы имеют необходимые свойства
        groups.value = rawGroups.filter(group => 
          group && 
          typeof group === 'object' && 
          group.id && 
          group.name
        )
      } catch (error) {
        console.error('Ошибка загрузки групп:', error)
        groups.value = []
      } finally {
        loading.value = false
      }
    }
    
    const loadLevels = async () => {
      try {
        const response = await axios.get('/api/levels/')
        
        // API возвращает данные в формате { count, next, previous, results: [...] }
        const rawLevels = response.data?.results || response.data || []
        
        // Проверяем, что все уровни имеют необходимые свойства
        levels.value = rawLevels.filter(level => 
          level && 
          typeof level === 'object' && 
          level.id && 
          level.name
        )
      } catch (error) {
        console.error('Ошибка загрузки уровней:', error)
        levels.value = []
      }
    }
    
    const loadDaysOfWeek = async () => {
      try {
        const response = await axios.get('/api/days/')
        const rawDays = response.data?.results || response.data || []
        
        daysOfWeek.value = rawDays.filter(day => 
          day && 
          typeof day === 'object' && 
          day.id && 
          day.name
        )
        console.log('Загружены дни недели:', daysOfWeek.value)
      } catch (error) {
        console.error('Ошибка загрузки дней недели:', error)
        daysOfWeek.value = []
      }
    }
    
    const loadTimeSlots = async () => {
      try {
        const response = await axios.get('/api/timeslots/')
        const rawTimeSlots = response.data?.results || response.data || []
        
        timeSlots.value = rawTimeSlots.filter(slot => 
          slot && 
          typeof slot === 'object' && 
          slot.id && 
          slot.start_time && 
          slot.end_time
        )
        console.log('Загружены временные слоты:', timeSlots.value)
      } catch (error) {
        console.error('Ошибка загрузки временных слотов:', error)
        timeSlots.value = []
      }
    }
    
    const getDayName = (dayId) => {
      const day = daysOfWeek.value.find(d => d.id === dayId)
      if (!day) return ''
      
      // Переводим дни недели на русский
      const dayTranslations = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник', 
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
      }
      
      return dayTranslations[day.name.toLowerCase()] || day.name
    }
    
    const getTimeSlotText = (timeId) => {
      const slot = timeSlots.value.find(s => s.id === timeId)
      return slot ? `${slot.start_time}-${slot.end_time}` : ''
    }
    
    const hasScheduleData = computed(() => {
      return selectedDays.value.some(dayId => 
        scheduleData.value[dayId] && scheduleData.value[dayId].length > 0
      )
    })
    
    // Инициализируем scheduleData для новых дней
    watch(selectedDays, (newDays, oldDays) => {
      newDays.forEach(dayId => {
        if (!scheduleData.value[dayId]) {
          scheduleData.value[dayId] = []
        }
      })
      
      // Удаляем данные для дней, которые больше не выбраны
      Object.keys(scheduleData.value).forEach(dayId => {
        if (!newDays.includes(parseInt(dayId))) {
          delete scheduleData.value[dayId]
        }
      })
    }, { deep: true })
    
    const parseExistingSchedule = (scheduleText) => {
      if (!scheduleText) return { selectedDays: [], scheduleData: {} }
      
      console.log('Парсинг расписания:', scheduleText)
      console.log('Доступные дни:', daysOfWeek.value)
      console.log('Доступные временные слоты:', timeSlots.value)
      
      const selectedDays = []
      const scheduleData = {}
      
      // Парсим расписание в формате "День: время1, время2; День2: время3"
      const scheduleParts = scheduleText.split(';')
      
      scheduleParts.forEach(part => {
        const [dayPart, timePart] = part.split(':')
        if (dayPart && timePart) {
          const dayName = dayPart.trim().toLowerCase()
          const times = timePart.trim().split(',').map(t => t.trim())
          
          console.log('Парсинг дня:', dayName, 'времена:', times)
          
          // Находим ID дня по названию
          const day = daysOfWeek.value.find(d => {
            const translatedName = getDayName(d.id).toLowerCase()
            return translatedName === dayName
          })
          
          if (day) {
            console.log('Найден день:', day)
            selectedDays.push(day.id)
            
            // Находим ID временных слотов по времени
            const timeIds = []
            times.forEach(time => {
              const timeSlot = timeSlots.value.find(slot => {
                const slotTime = `${slot.start_time}-${slot.end_time}`
                return slotTime === time
              })
              if (timeSlot) {
                console.log('Найден временной слот:', timeSlot)
                timeIds.push(timeSlot.id)
              }
            })
            
            if (timeIds.length > 0) {
              scheduleData[day.id] = timeIds
            }
          }
        }
      })
      
      console.log('Результат парсинга:', { selectedDays, scheduleData })
      return { selectedDays, scheduleData }
    }
    
    const editGroup = async (group) => {
      if (!group) return
      
      // Копируем данные группы и исправляем level_id
      form.value = { 
        ...group,
        level_id: group.level?.id || group.level_id || ''
      }
      
      // Сбрасываем данные расписания
      selectedDays.value = []
      scheduleData.value = {}
      
      // Убеждаемся, что данные загружены
      if (daysOfWeek.value.length === 0) {
        await loadDaysOfWeek()
      }
      if (timeSlots.value.length === 0) {
        await loadTimeSlots()
      }
      
      // Парсим существующее расписание
      const { selectedDays: parsedDays, scheduleData: parsedScheduleData } = parseExistingSchedule(group.schedule)
      selectedDays.value = parsedDays
      scheduleData.value = parsedScheduleData
      
      showEditModal.value = true
    }
    
    const deleteGroup = async (group) => {
      if (!group) return
      if (!confirm(`Вы уверены, что хотите удалить группу "${group.name}"?`)) return
      
      try {
        await axios.delete(`/api/groups/${group.id}/`)
        await loadGroups()
      } catch (error) {
        console.error('Ошибка удаления группы:', error)
      }
    }
    
    const submitForm = async () => {
      submitting.value = true
      try {
        // Генерируем расписание из выбранных дней и времени
        const scheduleText = generateScheduleText()
        
        const formData = {
          ...form.value,
          schedule: scheduleText
        }
        
        if (showEditModal.value && form.value.id) {
          await axios.put(`/api/groups/${form.value.id}/`, formData)
        } else {
          await axios.post('/api/groups/', formData)
        }
        
        await loadGroups()
        closeModal()
      } catch (error) {
        console.error('Ошибка сохранения группы:', error)
      } finally {
        submitting.value = false
      }
    }
    
    const generateScheduleText = () => {
      if (!hasScheduleData.value) {
        return ''
      }
      
      const scheduleParts = []
      
      selectedDays.value.forEach(dayId => {
        const dayName = getDayName(dayId)
        const timeIds = scheduleData.value[dayId] || []
        
        if (timeIds.length > 0) {
          const timeTexts = timeIds.map(timeId => getTimeSlotText(timeId))
          scheduleParts.push(`${dayName}: ${timeTexts.join(', ')}`)
        }
      })
      
      return scheduleParts.join('; ')
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      form.value = {
        name: '',
        level_id: '',
        total_capacity: 1,
        current_participants: 0,
        description: '',
        start_date: '',
        schedule: '',
        is_active: true
      }
      selectedDays.value = []
      scheduleData.value = {}
    }
    
    // Автоматическая загрузка при изменении фильтров
    watch(filters, () => {
      loadGroups()
    }, { deep: true })
    
    onMounted(() => {
      loadGroups()
      loadLevels()
      loadDaysOfWeek()
      loadTimeSlots()
    })
    
    return {
      groups,
      levels,
      daysOfWeek,
      timeSlots,
      loading,
      showCreateModal,
      showEditModal,
      submitting,
      filters,
      form,
      selectedDays,
      scheduleData,
      hasScheduleData,
      getDayName,
      getTimeSlotText,
      editGroup,
      deleteGroup,
      submitForm,
      closeModal
    }
  }
}
</script>

