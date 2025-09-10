

// KS Widget - Виджет расписания корейского языка
(function() {
    'use strict';
    
    // Конфигурация API
    const API_BASE = 'http://localhost:8000/api';
    
    // Компонент виджета
    const KSScheduleWidget = {
        template: `
            <div class="ks-widget-container">
                
                <!-- Фильтры -->
                <div v-if="!loading && groups.length > 0" class="filters">
                    <button @click="setFilter('all')" 
                            :class="['filter-btn', { 'active': currentFilter === 'all' }]">
                        Все группы
                    </button>
                    <button @click="setFilter('beginner')" 
                            :class="['filter-btn', { 'active': currentFilter === 'beginner' }]">
                        Начинающие
                    </button>
                    <button @click="setFilter('intermediate')" 
                            :class="['filter-btn', { 'active': currentFilter === 'intermediate' }]">
                        Средний уровень
                    </button>
                    <button @click="setFilter('advanced')" 
                            :class="['filter-btn', { 'active': currentFilter === 'advanced' }]">
                        Продвинутые
                    </button>
                </div>
                
                <!-- Расписание -->
                <div v-if="!loading && groups.length > 0" class="schedule-container">
                    <!-- Заголовки дней недели -->
                    <div class="schedule-header">
                        <div class="time-header"></div>
                        <div class="day-header">Понедельник</div>
                        <div class="day-header">Вторник</div>
                        <div class="day-header">Среда</div>
                        <div class="day-header">Четверг</div>
                        <div class="day-header">Пятница</div>
                        <div class="day-header">Суббота</div>
                        <div class="day-header">Воскресенье</div>
                    </div>
                    
                    <!-- Сетка расписания -->
                    <div class="schedule-grid">
                        <!-- Временные слоты -->
                        <div v-for="timeSlot in allTimeSlots" :key="timeSlot" 
                             :class="['time-row', { 'compact': !timeSlots.includes(timeSlot) }]">
                            <div class="time-label">{{ timeSlot }}</div>
                            
                            <!-- Ячейки для каждого дня -->
                            <div v-for="day in weekDays" :key="day" class="day-cell">
                                <div v-for="group in getFilteredGroupsForTimeAndDay(timeSlot, day)" :key="group.id" 
                                     class="group-block"
                                     :class="[
                                         'group-level-' + group.level.id, 
                                         { 'group-full': group.available_spots === 0 }
                                     ]"
                                     @mouseenter="hoverGroup = group.id"
                                     @mouseleave="hoverGroup = null">
                                    
                                    <!-- Идентификатор группы -->
                                    <div class="group-id">
                                        {{ group.shortName }}
                                    </div>
                                    
                                    <!-- Уровень -->
                                    <div class="group-title">{{ group.level.name }}</div>
                                    
                                    <!-- Места с прогресс-баром -->
                                    <div class="group-spots">
                                        <div class="spots-info">
                                            <span class="spots-text">{{ group.available_spots }}/{{ group.total_capacity }}</span>
                                            <span class="spots-label">мест</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" 
                                                 :style="{ width: (group.available_spots / group.total_capacity * 100) + '%' }"></div>
                                        </div>
                                    </div>
                                    
                                    <!-- Кнопка подробнее -->
                                    <button @click="showGroupDetails(group)" 
                                            class="group-button">
                                        Подробнее
                                    </button>
                                    
                                    <!-- Эффект при наведении -->
                                    <div v-if="hoverGroup === group.id" class="hover-effect"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Индикатор загрузки -->
                <div v-if="loading" class="loading">
                    <div class="loading-spinner"></div>
                    <div>
                        <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">Загрузка данных...</h3>
                        <p style="color: var(--text-secondary); margin: 0;">Подключаемся к серверу</p>
                    </div>
                </div>
                
                <!-- Сообщение об отсутствии групп -->
                <div v-else-if="groups.length === 0" style="text-align: center; padding: 4rem;">
                    <div style="background: var(--bg-accent); border: 1px solid var(--border-accent); border-radius: var(--border-radius-lg); padding: 2rem;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
                        <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">Нет доступных групп</h3>
                        <p style="color: var(--text-secondary); margin: 0;">Данные загружаются из API. Проверьте подключение к серверу.</p>
                    </div>
                </div>
                
                <!-- Модальное окно с описанием группы -->
                <div v-if="showGroupDetailsModal" class="modal-overlay">
                    <div class="modal-content">
                        <!-- Заголовок модального окна -->
                        <div class="modal-header">
                            <div>
                                <h3 class="modal-title">Информация о группе</h3>
                                <p class="modal-subtitle">Подробное описание группы</p>
                            </div>
                            <button @click="closeGroupDetailsModal" class="close-btn">
                                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                            
                        <!-- Информация о группе -->
                        <div v-if="selectedGroup">
                            <!-- Основная информация -->
                            <div class="info-block">
                                <h4 class="info-title">{{ selectedGroup.name }}</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                                    <div>
                                        <p class="info-text"><strong>Уровень:</strong> {{ selectedGroup.level.name }}</p>
                                        <p class="info-text"><strong>Доступно мест:</strong> {{ selectedGroup.available_spots }} из {{ selectedGroup.total_capacity }}</p>
                                    </div>
                                    <div>
                                        <p class="info-text"><strong>Дата начала:</strong> {{ formatDate(selectedGroup.start_date) }}</p>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Расписание -->
                            <div class="info-block">
                                <h5 class="info-title">Расписание занятий</h5>
                                <div v-if="getScheduleBlocks(selectedGroup).length > 0" class="schedule-blocks">
                                    <div v-for="block in getScheduleBlocks(selectedGroup)" :key="block.day" class="schedule-block">
                                        <div class="schedule-day">{{ block.dayName }}</div>
                                        <div class="schedule-times">
                                            <span v-for="time in block.times" :key="time" class="schedule-time">{{ time }}</span>
                                        </div>
                                    </div>
                                </div>
                                <p v-else class="info-text">Расписание не указано</p>
                            </div>
                            
                            <!-- Описание -->
                            <div class="info-block">
                                <h5 class="info-title">Описание курса</h5>
                                <p class="info-text">{{ selectedGroup.description || 'Описание курса будет добавлено позже.' }}</p>
                            </div>
                            
                            <!-- Кнопка записи -->
                            <div style="text-align: center;">
                                <button @click="showApplicationForm(selectedGroup)" 
                                        class="btn btn-primary"
                                        :disabled="selectedGroup.available_spots === 0">
                                    <span v-if="selectedGroup.available_spots === 0">Мест нет</span>
                                    <span v-else>Записаться в группу</span>
                                </button>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
                
                <!-- Модальное окно с формой заявки -->
                <div v-if="showApplicationModal" class="modal-overlay">
                    <div class="modal-content" style="max-width: 500px;">
                        <!-- Заголовок модального окна -->
                        <div class="modal-header">
                            <div>
                                <h3 class="modal-title">Запись в группу</h3>
                                <p class="modal-subtitle">Заполните форму для записи в группу</p>
                            </div>
                            <button @click="closeApplicationModal" class="close-btn">
                                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </button>
                        </div>
                        
                        <!-- Информация о группе -->
                        <div v-if="selectedGroup" class="info-block">
                            <h4 class="info-title">{{ selectedGroup.name }}</h4>
                            <p class="info-text">{{ getScheduleDisplay(selectedGroup) }}</p>
                            <p class="info-text"><strong>Доступно мест:</strong> {{ selectedGroup.available_spots }}</p>
                        </div>
                            
                        <form @submit.prevent="submitApplication">
                            <div class="form-group">
                                <label class="form-label">Имя *</label>
                                <input v-model="applicationForm.name" type="text" required class="form-input">
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Email *</label>
                                <input v-model="applicationForm.email" type="email" required class="form-input">
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Телефон</label>
                                <input v-model="applicationForm.phone" type="tel" class="form-input">
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Комментарий</label>
                                <textarea v-model="applicationForm.comment" rows="4" class="form-input form-textarea"
                                          placeholder="Расскажите о ваших целях изучения корейского языка..."></textarea>
                            </div>
                            
                            <div style="padding-top: 2rem; border-top: 2px solid var(--border-accent);">
                                <button type="submit" :disabled="submitting" class="btn btn-primary" style="width: 100%;">
                                    <span v-if="submitting" style="display: flex; align-items: center; justify-content: center;">
                                        <div class="loading-spinner"></div>
                                        Отправка...
                                    </span>
                                    <span v-else>Отправить заявку</span>
                                </button>
                            </div>
                        </form>
                        </div>
                    </div>
                </div>
                
                <!-- Уведомления -->
                <div v-if="notification.show" 
                     :class="['notification', notification.type === 'success' ? 'notification-success' : 'notification-error']">
                    <div style="display: flex; align-items: center;">
                        <div style="flex-shrink: 0; margin-right: 0.75rem;">
                            <svg v-if="notification.type === 'success'" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <svg v-else width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 0.875rem; font-weight: 500; margin: 0;">{{ notification.message }}</p>
                        </div>
                        <button @click="hideNotification" style="flex-shrink: 0; background: none; border: none; cursor: pointer; padding: 0.25rem;">
                            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `,
        
        data() {
            return {
                groups: [],
                weekDays: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                allTimeSlots: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
                timeSlots: ['15:00', '18:00'], // Активные временные слоты
                showApplicationModal: false,
                showGroupDetailsModal: false,
                selectedGroup: null,
                currentFilter: 'all',
                hoverGroup: null,
                loading: true,
                applicationForm: {
                    name: '',
                    email: '',
                    phone: '',
                    comment: '',
                    group_id: null
                },
                submitting: false,
                notification: {
                    show: false,
                    message: '',
                    type: 'success'
                }
            };
        },
        
        async mounted() {
            await this.loadData();
            this.updateActiveTimeSlots();
        },
        
        methods: {
            async loadData() {
                this.loading = true;
                try {
                    console.log('Загружаем данные из API...');
                    // Загружаем группы через публичный API
                    const groupsResponse = await fetch(`${API_BASE}/groups/public/`);
                    if (!groupsResponse.ok) throw new Error('Ошибка загрузки групп');
                    const groupsData = await groupsResponse.json();
                    
                    console.log('Получены данные из API:', groupsData);
                    
                    // Добавляем короткие названия и цвета для групп
                    this.groups = groupsData.map(group => ({
                        ...group,
                        shortName: this.generateShortName(group.name),
                        color: this.getGroupColor(group.level.id)
                    }));
                    
                    console.log('Обработанные группы:', this.groups);
                } catch (error) {
                    console.error('Ошибка загрузки данных:', error);
                    this.showNotification('Ошибка загрузки данных. Проверьте подключение к серверу.', 'error');
                    this.groups = [];
                } finally {
                    this.loading = false;
                }
            },
            
            generateShortName(name) {
                // Возвращаем полное название без сокращения
                return name;
            },
            
            getGroupColor(levelId) {
                // Цвета для разных уровней
                const colors = {
                    1: '#10B981', // Зеленый для начинающих
                    2: '#F59E0B', // Желтый для средних
                    3: '#EF4444'  // Красный для продвинутых
                };
                return colors[levelId] || '#3B82F6';
            },
            
            getGroupsForTimeAndDay(timeSlot, day) {
                // Фильтруем группы по времени и дню недели
                return this.groups.filter(group => {
                    if (!group.schedule) return false;
                    
                    // Если расписание в новом формате (объект)
                    if (typeof group.schedule === 'object' && group.schedule !== null) {
                        const daySchedule = group.schedule[day];
                        if (daySchedule && Array.isArray(daySchedule)) {
                            return daySchedule.includes(timeSlot);
                        }
                        return false;
                    }
                    
                    // Fallback для старого формата (строка)
                    const schedule = group.schedule.toLowerCase();
                    const dayName = this.getDayName(day);
                    
                    // Проверяем, есть ли группа в этот день
                    if (!schedule.includes(dayName.toLowerCase())) return false;
                    
                    // Проверяем время более точно
                    const timeMatch = schedule.includes(timeSlot) || 
                                   schedule.includes(timeSlot.replace(':', ''));
                    
                    return timeMatch;
                });
            },
            
            getFilteredGroupsForTimeAndDay(timeSlot, day) {
                // Получаем группы с учетом фильтра
                let groups = this.getGroupsForTimeAndDay(timeSlot, day);
                
                if (this.currentFilter !== 'all') {
                    const levelMap = {
                        'beginner': 1,
                        'intermediate': 2,
                        'advanced': 3
                    };
                    
                    groups = groups.filter(group => group.level.id === levelMap[this.currentFilter]);
                }
                
                console.log(`Группы для ${day} в ${timeSlot}:`, groups);
                return groups;
            },
            
            setFilter(filter) {
                this.currentFilter = filter;
            },
            
            getLevelEmoji(levelId) {
                const emojis = {
                    1: '🌱', // Начинающие
                    2: '🌿', // Средний уровень
                    3: '🌳'  // Продвинутые
                };
                return emojis[levelId] || '📚';
            },
            
            updateActiveTimeSlots() {
                // Собираем все временные слоты, которые используются в группах
                const usedTimeSlots = new Set();
                
                this.groups.forEach(group => {
                    if (group.schedule) {
                        // Если расписание в новом формате (объект)
                        if (typeof group.schedule === 'object' && group.schedule !== null) {
                            Object.values(group.schedule).forEach(daySchedule => {
                                if (Array.isArray(daySchedule)) {
                                    daySchedule.forEach(timeSlot => {
                                        usedTimeSlots.add(timeSlot);
                                    });
                                }
                            });
                        } else {
                            // Fallback для старого формата (строка)
                            const schedule = group.schedule.toLowerCase();
                            this.allTimeSlots.forEach(timeSlot => {
                                if (schedule.includes(timeSlot) || schedule.includes(timeSlot.replace(':', ''))) {
                                    usedTimeSlots.add(timeSlot);
                                }
                            });
                        }
                    }
                });
                
                // Обновляем активные временные слоты
                this.timeSlots = Array.from(usedTimeSlots).sort();
                console.log('Активные временные слоты:', this.timeSlots);
                
                // Если нет активных слотов, показываем сообщение
                if (this.timeSlots.length === 0) {
                    console.log('Нет активных временных слотов');
                }
            },
            
            getDayName(day) {
                const dayNames = {
                    'monday': 'понедельник',
                    'tuesday': 'вторник',
                    'wednesday': 'среда',
                    'thursday': 'четверг',
                    'friday': 'пятница',
                    'saturday': 'суббота',
                    'sunday': 'воскресенье'
                };
                return dayNames[day] || day;
            },
            
            getScheduleDisplay(group) {
                if (typeof group.schedule === 'object' && group.schedule !== null) {
                    const scheduleParts = [];
                    Object.entries(group.schedule).forEach(([day, times]) => {
                        if (Array.isArray(times) && times.length > 0) {
                            const dayName = this.getDayName(day);
                            const timesStr = times.join(', ');
                            scheduleParts.push(`${dayName} ${timesStr}`);
                        }
                    });
                    return scheduleParts.join('; ');
                }
                return group.schedule || 'Расписание не указано';
            },

            getScheduleBlocks(group) {
                if (!group.schedule) return [];
                
                if (typeof group.schedule === 'object' && group.schedule !== null) {
                    const scheduleBlocks = [];
                    const dayOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
                    
                    dayOrder.forEach(day => {
                        if (group.schedule[day] && Array.isArray(group.schedule[day]) && group.schedule[day].length > 0) {
                            scheduleBlocks.push({
                                day: day,
                                dayName: this.getDayName(day),
                                times: group.schedule[day]
                            });
                        }
                    });
                    
                    return scheduleBlocks;
                }
                
                return [];
            },
            
            formatDate(dateString) {
                if (!dateString) return 'Не указана';
                const date = new Date(dateString);
                return date.toLocaleDateString('ru-RU', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            },
            
            showGroupDetails(group) {
                this.selectedGroup = group;
                this.showGroupDetailsModal = true;
            },
            
            closeGroupDetailsModal() {
                this.showGroupDetailsModal = false;
                this.selectedGroup = null;
            },
            
            showApplicationForm(group) {
                this.selectedGroup = group;
                this.applicationForm.group_id = group.id;
                this.showApplicationModal = true;
                this.showGroupDetailsModal = false; // Закрываем окно с описанием
            },
            
            closeApplicationModal() {
                this.showApplicationModal = false;
                this.selectedGroup = null;
                this.applicationForm = {
                    name: '',
                    email: '',
                    phone: '',
                    comment: '',
                    group_id: null
                };
            },
            
            async submitApplication() {
                this.submitting = true;
                
                try {
                    const response = await fetch(`${API_BASE}/applications/create_public/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(this.applicationForm)
                    });
                    
                    if (response.ok) {
                        this.showNotification('Заявка отправлена', 'success');
                        this.closeApplicationModal();
                        await this.loadData();
                    } else {
                        const error = await response.json();
                        this.showNotification(error.detail || 'Ошибка отправки заявки', 'error');
                    }
                } catch (error) {
                    console.error('Ошибка отправки заявки:', error);
                    this.showNotification('Ошибка отправки заявки', 'error');
                } finally {
                    this.submitting = false;
                }
            },
            
            showNotification(message, type = 'success') {
                this.notification = {
                    show: true,
                    message,
                    type
                };
                
                setTimeout(() => {
                    this.hideNotification();
                }, 3000);
            },
            
            hideNotification() {
                this.notification.show = false;
            }
        }
    };
    
    // Функция для инициализации виджета
    function initWidget(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            const app = Vue.createApp(KSScheduleWidget);
            app.mount(container);
        }
    }
    
    // Функция для создания виджета в указанном элементе
    function createWidget(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            const app = Vue.createApp(KSScheduleWidget);
            app.mount(element);
        });
    }
    
    // Автоматическая инициализация при загрузке страницы
    document.addEventListener('DOMContentLoaded', function() {
        // Ищем элементы с классом ks-widget
        createWidget('.ks-widget');
        
        // Ищем элементы с атрибутом data-ks-widget
        createWidget('[data-ks-widget]');
    });
    
    // Экспортируем функции для использования в других скриптах
    window.KSScheduleWidget = {
        init: initWidget,
        create: createWidget,
        component: KSScheduleWidget
    };
    
})();