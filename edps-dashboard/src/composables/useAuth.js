import { useAuthStore } from '@/stores/authStore'
import { computed } from 'vue'
import { useToast } from 'vue-toastification'

export function useAuth() {
    const authStore = useAuthStore()
    const toast = useToast()

    // Computed property to get the user data
    const user = computed(() => authStore.user)

    // Computed property to check if user is authenticated
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    // Handle login
    const login = async (email, password, remember = false) => {
        try {
            await authStore.login(email, password, remember, toast)
            return { success: true }
        } catch (error) {
            return {
                success: false,
                message: error.message || 'Login failed. Please try again.'
            }
        }
    }

    // Handle logout
    const logout = async () => {
        authStore.logout()
        return { success: true }
    }

    return {
        user,
        isAuthenticated,
        login,
        logout
    }
} 