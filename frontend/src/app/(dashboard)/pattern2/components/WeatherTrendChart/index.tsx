import { useMemo } from "react";
import { usePattern2Context } from "../Pattern2Dashboard/context";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_temp' | 'avg_humidity' | 'total_precip' | 'avg_wind' | 'avg_pressure',
    title: string,
    color: string,
    yAxisTitle: string
}

function WeatherTrendChart({ dataType, title, color, yAxisTitle }: IProps) {
    const { correlationData } = usePattern2Context();

    const { dates, values } = useMemo(() => {
        const dates: string[] = [];
        const values: number[] = [];

        if (correlationData?.data?.data && Array.isArray(correlationData.data.data)) {
            correlationData.data.data.forEach(item => {
                if (item.date && item[dataType] !== undefined) {
                    const date = new Date(item.date);
                    dates.push(date.toISOString().split('T')[0]);
                    values.push(item[dataType]);
                }
            });
        }

        return { dates, values };
    }, [correlationData, dataType]);

    if (!dates.length || !values.length) {
        return <div>No data available</div>;
    }

    return (
        <Plot
            className='w-full'
            data={[
                {
                    x: dates,
                    y: values,
                    type: 'scatter',
                    mode: 'lines',
                    line: { 
                        color: '#ff6b6b',
                        width: 1.5
                    },
                    name: 'Daily Temperature'
                },
            ]}
            layout={{
                autosize: true,
                height: 300,
                title: {
                    text: 'Daily Average Temperature (2023-11-20 - 2024-12-03)',
                    font: { 
                        size: 16,
                        color: '#2d3436'
                    }
                },
                margin: { l: 50, r: 20, t: 40, b: 50 },
                xaxis: {
                    title: 'Date',
                    tickangle: 45,
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false
                },
                yaxis: {
                    title: 'Temperature (°C)',
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false
                },
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                showlegend: false,
                hovermode: 'x unified'
            }}
            useResizeHandler
            style={{ width: '100%' }}
            config={{
                displayModeBar: false
            }}
        />
    );
}

export default WeatherTrendChart; 