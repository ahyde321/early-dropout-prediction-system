<template>
  <div class="fixed bottom-4 right-4 z-[9999]">
    <!-- Floating Chat Button -->
    <button
      v-if="!isOpen"
      @click="toggleChat"
      class="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700 transition-all duration-300 flex items-center justify-center"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
        />
      </svg>
    </button>

    <!-- Chat Window -->
    <div
      v-if="isOpen"
      class="bg-white rounded-lg shadow-xl w-96 h-[600px] flex flex-col fixed bottom-4 right-4"
    >
      <!-- Chat Header -->
      <div class="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h3 class="font-semibold">EDPS Advisor Assistant</h3>
        <button @click="toggleChat" class="text-white hover:text-gray-200">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <!-- Chat Messages -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'flex',
            message.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            :class="[
              'max-w-[80%] rounded-lg p-3',
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-800'
            ]"
          >
            {{ message.content }}
          </div>
        </div>
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-gray-100 rounded-lg p-3 text-gray-800">
            <div class="flex space-x-2">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Input -->
      <div class="p-4 border-t">
        <form @submit.prevent="sendMessage" class="flex space-x-2">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type your message..."
            class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isLoading"
          />
          <button
            type="submit"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            :disabled="!newMessage.trim() || isLoading"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '../services/api'

export default {
  name: 'ChatWidget',
  setup() {
    const isOpen = ref(false)
    const messages = ref([])
    const newMessage = ref('')
    const isLoading = ref(false)

    const toggleChat = () => {
      isOpen.value = !isOpen.value
    }

    const sendMessage = async () => {
      if (!newMessage.value.trim() || isLoading.value) return

      const userMessage = {
        role: 'user',
        content: newMessage.value
      }

      messages.value.push(userMessage)
      newMessage.value = ''
      isLoading.value = true

      try {
        console.log('Sending request to endpoint:', api.defaults.baseURL + '/chatbot/chat')
        const response = await api.post('/chat', {
          messages: [...messages.value]
        })

        messages.value.push({
          role: 'assistant',
          content: response.data.response
        })
      } catch (error) {
        console.error('Error sending message:', error)
        console.error('Full error details:', {
          message: error.message,
          status: error.response?.status,
          url: error.config?.url,
          baseURL: api.defaults.baseURL
        })
        messages.value.push({
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.'
        })
      } finally {
        isLoading.value = false
      }
    }

    return {
      isOpen,
      messages,
      newMessage,
      isLoading,
      toggleChat,
      sendMessage
    }
  }
}
</script>

<style scoped>
.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}
</style>
