'use client'

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import { weatherApi } from '../api/weather';

const TemperatureDecomposition = () => {
    const chartRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchAndPlotData = async () => {
            try {
                const response = await weatherApi.getForecastWeather('Da Nang', 14);
                const hourlyData = response.data.forecast.forecastday.flatMap(day => day.hour);
                const times = hourlyData.map(hour => hour.time);
                const temperatures = hourlyData.map(hour => hour.temp_c);

                // Calculate trend using moving average
                const windowSize = 24;
                const trend = temperatures.map((_, index) => {
                    const start = Math.max(0, index - windowSize / 2);
                    const end = Math.min(temperatures.length, index + windowSize / 2);
                    const window = temperatures.slice(start, end);
                    return window.reduce((sum, val) => sum + val, 0) / window.length;
                });

                // Calculate seasonal pattern
                const seasonal = temperatures.map((temp, index) => {
                    const hourOfDay = new Date(times[index]).getHours();
                    const sameHourTemps = temperatures.filter((_, i) => 
                        new Date(times[i]).getHours() === hourOfDay
                    );
                    const avgTemp = sameHourTemps.reduce((sum, val) => sum + val, 0) / sameHourTemps.length;
                    return avgTemp - trend[index];
                });

                // Calculate residuals
                // const residuals = temperatures.map((temp, index) => 
                //     temp - trend[index] - seasonal[index]
                // );

                const traces = [
                    {
                        x: times,
                        y: temperatures,
                        name: 'Original Temperature',
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#ff7f0e', width: 1 }
                    },
                    {
                        x: times,
                        y: trend,
                        name: 'Trend',
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#1f77b4', width: 2 }
                    },
                    {
                        x: times,
                        y: seasonal,
                        name: 'Seasonal',
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#2ca02c', width: 1 }
                    },
                    // {
                    //     x: times,
                    //     y: residuals,
                    //     name: 'Residual',
                    //     type: 'scatter',
                    //     mode: 'markers',
                    //     marker: { 
                    //         color: '#d62728',
                    //         size: 3,
                    //         opacity: 0.7
                    //     }
                    // }
                ];

                const layout = {
                    grid: {
                        rows: 4,
                        columns: 1,
                        pattern: 'independent',
                        roworder: 'top to bottom'
                    },
                    height: 800,
                    margin: { t: 30, r: 50, l: 50, b: 30 },
                    showlegend: true,
                    ...traces.reduce((acc, _, i) => ({
                        ...acc,
                        [`xaxis${i + 1}`]: {
                            title: i === 3 ? 'Time' : '',
                            showgrid: true,
                            gridcolor: '#eee',
                            zeroline: i === 3
                        },
                        [`yaxis${i + 1}`]: {
                            title: traces[i].name,
                            showgrid: true,
                            gridcolor: '#eee',
                            zeroline: true,
                            zerolinecolor: '#888',
                            zerolinewidth: 1
                        }
                    }), {}),
                    plot_bgcolor: 'white',
                    paper_bgcolor: 'white'
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

    return <div ref={chartRef} />;
};

export default TemperatureDecomposition; 