export interface User {
    id: number
    username: string
    fullname: string
}

export interface UserCreate {
    username: string
    fullname: string
    password: string
}

export interface LoginResponse {
    access_token: string
}