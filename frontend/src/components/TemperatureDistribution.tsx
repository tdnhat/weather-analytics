'use client'

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import { weatherApi } from '../api/weather';

const TemperatureDistribution = () => {
    const chartRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchAndPlotData = async () => {
            try {
                const response = await weatherApi.getForecastWeather('Da Nang', 14);
                const hourlyData = response.data.forecast.forecastday.flatMap(day => day.hour);

                const traces = [
                    {
                        x: hourlyData.map(hour => hour.pressure_mb),
                        name: 'Pressure Station',
                        type: 'histogram',
                        opacity: 0.7,
                        marker: { color: '#1f77b4' }
                    },
                    {
                        x: hourlyData.map(hour => hour.humidity),
                        name: 'Relative Humidity',
                        type: 'histogram',
                        opacity: 0.7,
                        marker: { color: '#2ca02c' }
                    },
                    {
                        x: hourlyData.map(hour => hour.temp_c),
                        name: 'Temperature',
                        type: 'histogram',
                        opacity: 0.7,
                        marker: { color: '#d62728' }
                    }
                ];

                const layout = {
                    title: 'Weather Parameters Distribution',
                    barmode: 'overlay',
                    xaxis: { title: 'Value' },
                    yaxis: { title: 'Count' },
                    showlegend: true,
                    height: 600,
                    width: 800,
                    bargap: 0.1,
                    plot_bgcolor: 'white',
                    paper_bgcolor: 'white',
                };

                const config = {
                    responsive: true
                };

                Plotly.newPlot(chartRef.current!, traces, layout, config);
            } catch (error) {
                console.error('Error fetching or plotting data:', error);
            }
        };

        fetchAndPlotData();

        return () => {
            if (chartRef.current) {
                Plotly.purge(chartRef.current);
            }
        };
    }, []);

    return <div ref={chartRef} />;
};

export default TemperatureDistribution;