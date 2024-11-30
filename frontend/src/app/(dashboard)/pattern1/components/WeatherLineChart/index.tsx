import React, { useMemo } from 'react'
import { weatherRawTypesDto } from '@/api/weather/index'
import Plot from 'react-plotly.js'
import { usePattern1Context } from '../Pattern1Dashboard/context'

interface IProps { 
    dataType: 
    | 'avg_feelslike_c'
    | 'avg_temp_c'
    | 'avg_gust_kph'
    | 'avg_humidity'
    | 'avg_precip_mm'
    | 'avg_wind_kph'
    | 'avg_windchill_c',
    title?: string,
    color?: string
}

function WeatherLineChart({ dataType, title, color }: IProps) {
    const { weatherData, groupBy } = usePattern1Context()

    const { xList, yList } = useMemo(() => {
        let xList: number[] = []
        if (weatherData && weatherData.data) {
            if (groupBy === 'day') {
                xList = weatherData.data
                    .map(item => (item as { day: number }).day)
            } else if (groupBy === 'month') {
                xList = weatherData.data
                    .map(item => (item as { month: number }).month)
            } else if (groupBy === 'week') {
                xList = weatherData.data
                    .map(item => (item as { week: number }).week)
            }
        }

        const yList = weatherData?.data.map(data => data[dataType])
        
        return { xList, yList }
    }, [weatherData, groupBy])


    return (
        <Plot
            className='w-full'
            data={[
            {
                x: xList,
                y: yList,
                type: 'scatter',
                mode: 'lines',
                line: {color}
            },
            ]}
            layout={{
                width: 840, height: 320, title: {text: title || 'Line Chart'},
            }}
        />
    )
}

export default WeatherLineChart