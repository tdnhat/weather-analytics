'use client'

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import { weatherApi } from '../api/weather';

const WeatherCharts = () => {
    const chartRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchAndPlotData = async () => {
            try {
                const response = await weatherApi.getForecastWeather('Da Nang', 14);
                const hourlyData = response.data.forecast.forecastday.flatMap(day => day.hour);
                const times = hourlyData.map(hour => hour.time);

                const traces = [
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.temp_c),
                        name: 'Temperature (°C)',
                        type: 'scatter',
                        line: { color: '#ff7f0e', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.feelslike_c),
                        name: 'Feels Like (°C)',
                        type: 'scatter',
                        line: { color: '#1f77b4', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.windchill_c),
                        name: 'Wind Chill (°C)',
                        type: 'scatter',
                        line: { color: '#2ca02c', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.heatindex_c),
                        name: 'Heat Index (°C)',
                        type: 'scatter',
                        line: { color: '#d62728', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.dewpoint_c),
                        name: 'Dew Point (°C)',
                        type: 'scatter',
                        line: { color: '#9467bd', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.pressure_mb),
                        name: 'Pressure (mb)',
                        type: 'scatter',
                        line: { color: '#8c564b', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.precip_mm),
                        name: 'Precipitation (mm)',
                        type: 'scatter',
                        line: { color: '#e377c2', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.humidity),
                        name: 'Humidity (%)',
                        type: 'scatter',
                        line: { color: '#7f7f7f', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.cloud),
                        name: 'Cloud Cover (%)',
                        type: 'scatter',
                        line: { color: '#bcbd22', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.chance_of_rain),
                        name: 'Chance of Rain (%)',
                        type: 'scatter',
                        line: { color: '#17becf', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.vis_km),
                        name: 'Visibility (km)',
                        type: 'scatter',
                        line: { color: '#aec7e8', width: 1 }
                    },
                    {
                        x: times,
                        y: hourlyData.map(hour => hour.uv),
                        name: 'UV Index',
                        type: 'scatter',
                        line: { color: '#ffbb78', width: 1 }
                    }
                ];

                const layout = {
                    grid: {
                        rows: traces.length,
                        columns: 1,
                        pattern: 'independent',
                        roworder: 'top to bottom'
                    },
                    height: traces.length * 150,
                    margin: { t: 30, r: 50, l: 50, b: 30 },
                    showlegend: true,
                    ...traces.reduce((acc, _, i) => ({
                        ...acc,
                        [`xaxis${i + 1}`]: {
                            title: 'Time',
                            showgrid: true,
                            gridcolor: '#eee',
                            zeroline: false,
                            showticklabels: i === traces.length - 1
                        },
                        [`yaxis${i + 1}`]: {
                            title: 'Value',
                            showgrid: true,
                            gridcolor: '#eee',
                            zeroline: false
                        }
                    }), {}),
                    plot_bgcolor: 'white',
                    paper_bgcolor: 'white',
                };

                const config = {
                    responsive: true,
                    scrollZoom: true
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

    return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

export default WeatherCharts; 