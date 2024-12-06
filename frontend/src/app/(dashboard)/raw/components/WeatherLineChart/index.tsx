import { useMemo, useRef, useEffect, useState } from "react";
import { usePattern1Context } from "../Pattern1Dashboard/context";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_feelslike_c' | 'avg_temp_c' | 'avg_gust_kph' | 'avg_humidity' | 'avg_precip_mm' | 'avg_wind_kph' | 'avg_windchill_c',
    title?: string,
    color?: string
}

function WeatherLineChart({ dataType, title, color }: IProps) {
    const { weatherData } = usePattern1Context();
    const chartRef = useRef<HTMLDivElement>(null);
    const [containerWidth, setContainerWidth] = useState(0);

    useEffect(() => {
        const updateWidth = () => {
            if (chartRef.current) {
                setContainerWidth(chartRef.current.clientWidth);
            }
        };

        // Initial width
        updateWidth();

        // Create ResizeObserver
        const resizeObserver = new ResizeObserver(updateWidth);
        if (chartRef.current) {
            resizeObserver.observe(chartRef.current);
        }

        // Cleanup
        return () => resizeObserver.disconnect();
    }, []);

    const { xList, yList } = useMemo(() => {
        let xList: string[] = []
        let yList: number[] = []

        if (weatherData && weatherData.data) {
            xList = weatherData.data.map(item => {
                if ('day' in item) {
                    return `${item.day}/${item.month}/${item.year}`
                }
                if ('week' in item) {
                    return `Week ${item.week}/${item.year}`
                }
                return `${item.month}/${item.year}`
            })
            yList = weatherData.data.map(item => item[dataType])
        }

        return { xList, yList }
    }, [weatherData, dataType])

    return (
        <div ref={chartRef} className="w-full">
            <Plot
                className="w-full"
                data={[
                    {
                        x: xList,
                        y: yList,
                        type: 'scatter',
                        mode: 'lines',
                        line: { color },
                    },
                ]}
                layout={{
                    width: containerWidth,
                    height: 320,
                    title: { text: title || 'Weather Data Chart', font: { color: '#0e7490' } },
                    margin: { l: 50, r: 50, t: 50, b: 50 },
                    xaxis: {
                        tickfont: {
                            family: 'Arial, sans-serif',
                        },
                        tickangle: 45
                    },
                    hovermode: 'x unified',
                    showlegend: true,
                    paper_bgcolor: 'white',  // Set background to white
                    plot_bgcolor: 'white',   // Set plot area background to white
                }}
                config={{
                    responsive: true,
                    displayModeBar: true,
                }}
            />
        </div>
    )
}

export default WeatherLineChart;