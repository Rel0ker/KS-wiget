<template>
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <h1 class="text-xl font-semibold text-gray-900">KS Widget - Админ панель</h1>
        </div>
        
        <div class="flex items-center space-x-4">
          <nav class="flex space-x-8">
            <router-link 
              to="/dashboard" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              :class="{ 'text-blue-600': $route.path === '/dashboard' }"
            >
              Панель управления
            </router-link>
            
            <router-link 
              to="/groups" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              :class="{ 'text-blue-600': $route.path === '/groups' }"
            >
              Группы
            </router-link>
            
            <router-link 
              to="/applications" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              :class="{ 'text-blue-600': $route.path === '/applications' }"
            >
              Заявки
            </router-link>
          </nav>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">{{ user?.username }}</span>
            <button @click="logout" class="btn btn-secondary text-sm">
              Выйти
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Navigation',
  setup() {
    const authStore = useAuthStore()
    
    const user = computed(() => authStore.user)
    
    const logout = () => {
      authStore.logout()
    }
    
    return {
      user,
      logout
    }
  }
}
</script>
