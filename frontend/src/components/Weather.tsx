'use client'

import { useState, useEffect } from 'react';
import { weatherApi, WeatherResponse } from '../api/weather';

const Weather = () => {
    const [weather, setWeather] = useState<WeatherResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchWeather = async () => {
            try {
                setLoading(true);
                const response = await weatherApi.getCurrentWeather('London');
                setWeather(response.data);
            } catch (err) {
                setError('Failed to fetch weather data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchWeather();
    }, []);

    if (loading) return <div>Loading weather data...</div>;
    if (error) return <div>{error}</div>;
    if (!weather) return null;

    return (
        <div>
            <h2>{weather.location.name}, {weather.location.country}</h2>
            <div>Temperature: {weather.current.temp_c}°C / {weather.current.temp_f}°F</div>
            <div>Condition: {weather.current.condition.text}</div>
            <img 
                src={weather.current.condition.icon} 
                alt={weather.current.condition.text}
                width={100}
                height={100}
            />
            <div>Feels like: {weather.current.feelslike_c}°C / {weather.current.feelslike_f}°F</div>
            <div>Humidity: {weather.current.humidity}%</div>
            <div>Wind: {weather.current.wind_kph} km/h {weather.current.wind_dir}</div>
            <div>Last updated: {weather.current.last_updated}</div>
        </div>
    );
};

export default Weather; 