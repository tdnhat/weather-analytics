import axios from "axios";

export const apiInstance = axios.create({
    baseURL: process.env.WEATHER_API_BASE_URL
})

apiInstance.interceptors.request.use(
    (config) => {
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor
apiInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.log('Unauthorized')
        }
        return Promise.reject(error)
    }
)

export const req = apiInstance
export const httpGet = req.get
export const httpPost = req.post
export const httpPut = req.put
export const httpDelete = req.delete


