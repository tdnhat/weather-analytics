import { httpGet } from './axios'

// Define interfaces for the API response
interface Location {
    name: string;
    region: string;
    country: string;
    lat: number;
    lon: number;
    tz_id: string;
    localtime_epoch: number;
    localtime: string;
}

interface Condition {
    text: string;
    icon: string;
    code: number;
}

interface AirQuality {
    co: number;
    no2: number;
    o3: number;
    so2: number;
    "pm2_5": number;
    pm10: number;
    "us-epa-index": number;
    "gb-defra-index": number;
}

interface Current {
    last_updated_epoch: number;
    last_updated: string;
    temp_c: number;
    temp_f: number;
    is_day: number;
    condition: Condition;
    wind_mph: number;
    wind_kph: number;
    wind_degree: number;
    wind_dir: string;
    pressure_mb: number;
    pressure_in: number;
    precip_mm: number;
    precip_in: number;
    humidity: number;
    cloud: number;
    feelslike_c: number;
    feelslike_f: number;
    vis_km: number;
    vis_miles: number;
    uv: number;
    gust_mph: number;
    gust_kph: number;
    air_quality: AirQuality;
}

interface Day {
    maxtemp_c: number;
    mintemp_c: number;
    avgtemp_c: number;
    maxwind_kph: number;
    totalprecip_mm: number;
    avghumidity: number;
    condition: Condition;
    uv: number;
    air_quality: AirQuality;
}

interface Astro {
    sunrise: string;
    sunset: string;
    moonrise: string;
    moonset: string;
    moon_phase: string;
}

interface HourForecast {
    time: string;
    temp_c: number;
    feelslike_c: number;
    wind_kph: number;
    wind_dir: string;
    pressure_mb: number;
    precip_mm: number;
    humidity: number;
    cloud: number;
    windchill_c: number;
    heatindex_c: number;
    dewpoint_c: number;
    chance_of_rain: number;
    vis_km: number;
    uv: number;
    air_quality: AirQuality;
}

interface ForecastDay {
    date: string;
    day: Day;
    astro: Astro;
    hour: HourForecast[];
}

interface ForecastResponse extends WeatherResponse {
    forecast: {
        forecastday: ForecastDay[];
    };
}

export interface WeatherResponse {
    location: Location;
    current: Current;
}

export const weatherApi = {
    getCurrentWeather: async (city: string) => {
        try {
            const response = await httpGet<WeatherResponse>(`/current.json`, {
                params: {
                    key: process.env.WEATHER_API_KEY,
                    q: city,
                    aqi: 'yes'
                }
            }
            );
            // Validate response data
            if (!response.data) {
                throw new Error('No data received from weather API');
            }
            
            return response;
        } catch (error) {
            // Log the full error for debugging
            console.error('Weather API Error:', {
                error,
                city,
                timestamp: new Date().toISOString()
            });
            throw error;
        }
    },

    getForecastWeather: async (city: string, days: number = 1) => {
        try {
            const response = await httpGet<ForecastResponse>(`/forecast.json`, {
                params: {
                    key: process.env.WEATHER_API_KEY,
                    q: city,
                    days,
                    aqi: 'yes',
                    alerts: 'no'
                }
            });
            
            if (!response.data) {
                throw new Error('No data received from weather API');
            }
            
            console.log(response.data);
            return response;
        } catch (error) {
            console.error('Weather Forecast API Error:', {
                error,
                city,
                days,
                timestamp: new Date().toISOString()
            });
            throw error;
        }
    },
};