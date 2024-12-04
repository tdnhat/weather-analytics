import { useMemo } from "react";
import { usePattern2Context } from "../Pattern2Dashboard/context";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_temp' | 'avg_humidity' | 'total_precip' | 'avg_wind' | 'avg_pressure',
    title: string,
    yAxisTitle: string
}

function WeatherTrendChart({ dataType, title, yAxisTitle }: IProps) {
    const { correlationData } = usePattern2Context();

    const { dates, values, smoothedValues } = useMemo(() => {
        const dates: string[] = [];
        const values: number[] = [];
        
        if (correlationData?.data?.data && Array.isArray(correlationData.data.data)) {
            correlationData.data.data.forEach(item => {
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
                    y: smoothedValues,
                    type: 'scatter',
                    mode: 'lines',
                    line: { 
                        color: '#a29bfe',
                        width: 2.5,
                        shape: 'spline',
                    },
                    name: 'Trend',
                    hovertemplate: 'Date: %{x}<br>Trend: %{y:.2f}<extra></extra>'
                }
            ]}
            layout={{
                autosize: true,
                height: 300,
                title: {
                    text: title,
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
                    zeroline: false,
                    showspikes: true,
                    spikemode: 'across',
                    spikethickness: 1
                },
                yaxis: {
                    title: yAxisTitle,
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false,
                    showspikes: true,
                    spikethickness: 1
                },
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                showlegend: true,
                legend: {
                    x: 1,
                    xanchor: 'right',
                    y: 1,
                    bgcolor: 'rgba(255, 255, 255, 0.8)',
                    bordercolor: '#f5f6fa',
                    borderwidth: 1
                },
                hovermode: 'x unified',
            }}
            useResizeHandler
            style={{ width: '100%' }}
            config={{
                responsive: true
            }}
        />
    );
}

export default WeatherTrendChart; 