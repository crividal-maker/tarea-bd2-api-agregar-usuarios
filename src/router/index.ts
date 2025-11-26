import EditUser from '@/views/EditUser.vue'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import RegisterView from '@/views/RegisterView.vue'  
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    { name: 'home', path: '/', component: Home },
    { name: 'login', path: '/login', component: Login },
    { name: 'register', path: '/register', component: RegisterView }, 
    { name: 'userEdit', path: '/users/:id/edit/', component: EditUser },
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})