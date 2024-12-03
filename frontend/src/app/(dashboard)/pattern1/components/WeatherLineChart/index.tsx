import { useMemo } from "react";
import { usePattern1Context } from "../Pattern1Dashboard/context";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_feelslike_c' | 'avg_temp_c' | 'avg_gust_kph' | 'avg_humidity' | 'avg_precip_mm' | 'avg_wind_kph' | 'avg_windchill_c',
    title?: string,
    color?: string
}

function WeatherLineChart({ dataType, title, color }: IProps) {
    const { weatherData } = usePattern1Context();

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
        <Plot
            className='w-full'
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
                autosize: true,
                height: 320,
                title: { text: title || 'Weather Data Chart' },
                margin: { l: 50, r: 50, t: 50, b: 50 },
                xaxis: {
                    tickfont: {
                        family: 'Arial, sans-serif',
                    },
                    tickangle: 45
                },
                hovermode: 'x unified'
            }}
            useResizeHandler
        />
    )
}

export default WeatherLineChart;