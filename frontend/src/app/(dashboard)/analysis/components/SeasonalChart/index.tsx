import { useMemo, useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_temp' | 'avg_humidity' | 'total_precip' | 'avg_wind' | 'avg_pressure',
    title: string,
    yAxisTitle: string,
    data: any // Type this according to your data structure
}

function SeasonalChart({ dataType, title, yAxisTitle, data }: IProps) {
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

    const plotData = useMemo(() => {
        const quarterlyData: { [key: string]: { dates: string[], values: number[], quarter: number } } = {};
        
        if (data?.data && Array.isArray(data.data)) {
            data.data.forEach(item => {
                const key = `${item.year}-Q${item.quarter}`;
                if (!quarterlyData[key]) {
                    quarterlyData[key] = { dates: [], values: [], quarter: item.quarter };
                }
                quarterlyData[key].dates.push(item.date || '');
                quarterlyData[key].values.push(item[dataType] || 0);
            });
        }

        const quarterColors = {
            1: '#4caf50',  // softer green
            2: '#f39c12',  // yellow/orange
            3: '#e67e22',  // softer orange 
            4: '#2980b9'   // blue
        };

        return Object.entries(quarterlyData).map(([key, data]) => ({
            x: data.dates,
            y: data.values,
            type: 'scatter',
            mode: 'lines+markers',
            name: key,
            line: {
                shape: 'spline',
                width: 2,
                color: quarterColors[data.quarter as keyof typeof quarterColors]
            },
            marker: {
                size: 6,
                opacity: 0.7
            }
        }));
    }, [data, dataType]);

    return (
        <div ref={chartRef} className="w-full">
            <Plot
                data={plotData}
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

export default SeasonalChart;