<script setup lang="ts">
import type { UserCreate } from '@/interfaces'
import { registerUser } from '@/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userData = ref({
    username: '',
    fullname: '',
    password: '',
    confirmPassword: '',
})
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

async function register() {
    // Validaciones
    if (!userData.value.username || !userData.value.fullname || !userData.value.password) {
        error.value = 'Todos los campos son obligatorios'
        return
    }

    if (userData.value.password !== userData.value.confirmPassword) {
        error.value = 'Las contraseñas no coinciden'
        return
    }

    if (userData.value.password.length < 6) {
        error.value = 'La contraseña debe tener al menos 6 caracteres'
        return
    }

    loading.value = true
    error.value = ''

    try {
        const newUser = await registerUser({
            username: userData.value.username,
            fullname: userData.value.fullname,
            password: userData.value.password,
        } as UserCreate)

        if (newUser) {
            // Registro exitoso - redirigir al login
            router.push({ name: 'login' })
        } else {
            error.value = 'Error al crear el usuario. El nombre de usuario puede estar en uso.'
        }
    } catch (err) {
        error.value = 'Error al conectar con el servidor'
    } finally {
        loading.value = false
    }
}

function goToLogin() {
    router.push({ name: 'login' })
}
</script>

<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="8" lg="6">
                <v-card elevation="4">
                    <v-card-title class="bg-primary pa-6">
                        <v-icon icon="mdi-account-plus" size="large" class="mr-3"></v-icon>
                        <span class="text-h4">Registro de Usuario</span>
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-alert
                            v-if="error"
                            type="error"
                            variant="tonal"
                            closable
                            class="mb-4"
                            @click:close="error = ''"
                        >
                            {{ error }}
                        </v-alert>

                        <v-form @submit.prevent="register">
                            <v-text-field
                                v-model="userData.username"
                                label="Usuario"
                                prepend-inner-icon="mdi-account"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                required
                                class="mb-4"
                            ></v-text-field>

                            <v-text-field
                                v-model="userData.fullname"
                                label="Nombre completo"
                                prepend-inner-icon="mdi-card-account-details"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                required
                                class="mb-4"
                            ></v-text-field>

                            <v-text-field
                                v-model="userData.password"
                                label="Contraseña"
                                prepend-inner-icon="mdi-lock"
                                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                :type="showPassword ? 'text' : 'password'"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                required
                                class="mb-4"
                                @click:append-inner="showPassword = !showPassword"
                            ></v-text-field>

                            <v-text-field
                                v-model="userData.confirmPassword"
                                label="Confirmar contraseña"
                                prepend-inner-icon="mdi-lock-check"
                                :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                :type="showConfirmPassword ? 'text' : 'password'"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                required
                                class="mb-4"
                                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                            ></v-text-field>

                            <v-divider class="my-6"></v-divider>

                            <div class="d-flex flex-column gap-3">
                                <v-btn
                                    type="submit"
                                    color="primary"
                                    size="large"
                                    prepend-icon="mdi-account-plus"
                                    :loading="loading"
                                    block
                                >
                                    Registrarse
                                </v-btn>

                                <v-btn
                                    color="grey"
                                    size="large"
                                    variant="text"
                                    prepend-icon="mdi-login"
                                    @click="goToLogin"
                                    :disabled="loading"
                                    block
                                >
                                    ¿Ya tienes cuenta? Inicia sesión
                                </v-btn>
                            </div>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>