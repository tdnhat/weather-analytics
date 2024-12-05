import { useMemo, useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_temp' | 'avg_humidity' | 'total_precip' | 'avg_wind' | 'avg_pressure',
    title: string,
    yAxisTitle: string,
    data: any // Type this according to your data structure
}

function WeatherTrendChart({ dataType, title, yAxisTitle, data }: IProps) {
    const chartRef = useRef<HTMLDivElement>(null);
    const [containerWidth, setContainerWidth] = useState(0);

    useEffect(() => {
        const updateWidth = () => {
            if (chartRef.current) {
                setContainerWidth(chartRef.current.clientWidth);
            }
        };

        const resizeObserver = new ResizeObserver(updateWidth);
        if (chartRef.current) {
            resizeObserver.observe(chartRef.current);
        }

        return () => resizeObserver.disconnect();
    }, []);

    const { dates, values, smoothedValues } = useMemo(() => {
        const dates: string[] = [];
        const values: number[] = [];
        
        if (data?.data && Array.isArray(data.data)) {
            data.data.forEach(item => {
                if (item.date && item[dataType] !== undefined) {
                    dates.push(item.date);
                    values.push(item[dataType]);
                }
            });
        }

        const windowSize = 30;
        const smoothedValues = values.map((_, index) => {
            if (index < windowSize - 1) {
                const availableWindow = values.slice(0, index + 1);
                return availableWindow.reduce((sum, val) => sum + val, 0) / availableWindow.length;
            }
            
            let weightedSum = 0;
            let weightSum = 0;
            
            for (let i = 0; i < windowSize; i++) {
                const weight = Math.exp(-Math.pow(i - windowSize/2, 2) / (windowSize * 2));
                weightedSum += values[index - i] * weight;
                weightSum += weight;
            }
            
            return weightedSum / weightSum;
        });

        return { dates, values, smoothedValues };
    }, [data, dataType]);

    return (
        <div ref={chartRef} className="w-full bg-clip-padding backdrop-filter backdrop-blur-lg bg-opacity-30 border border-gray-100 rounded-lg p-4">
            <Plot
                data={[
                    {
                        x: dates,
                        y: smoothedValues,
                        type: 'scatter',
                        mode: 'lines',
                        line: { 
                            color: '#a29bfe',
                            width: 2.5,
                            shape: 'spline',
                        },
                        name: 'Trend',
                    }
                ]}
                layout={{
                    width: containerWidth,
                    height: 400,
                    title: {
                        text: title,
                        font: { size: 16, color: '#0e7490' },
                    },
                    margin: { l: 50, r: 20, t: 40, b: 50 },
                    xaxis: {
                        title: {
                            text: 'Date',
                            font: { color: '#0e7490' }
                        },
                        tickangle: 45,
                        showgrid: true,
                        tickfont: {
                            color: '#0e7490'
                        }
                    },
                    yaxis: {
                        title: {
                            text: yAxisTitle,
                            font: { color: '#0e7490' }
                        },
                        showgrid: true,
                        tickfont: {
                            color: '#0e7490'
                        }
                    },
                    showlegend: true,
                    hovermode: 'x unified',
                    paper_bgcolor: 'white',
                    plot_bgcolor: 'white',
                }}
                config={{
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                }}
            />
        </div>
    );
}

export default WeatherTrendChart;