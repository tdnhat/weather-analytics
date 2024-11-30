import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawQueries } from '@/entities/weatherRaw/queries'
import { Pattern1Provider } from './context'
import WeatherLineChart from '../WeatherLineChart'
import WeatherDashboardControls from '../WeatherDashboardControls'

function Pattern1Dashboard() {
    const [groupBy, setGroupBy] = useState<'day' | 'month' | 'week'>('day')
    const [filter, setFilter] = useState<{start_date: string, end_date: string, group_by: 'day' | 'month' | 'week'}>({
        start_date: '2024-10-01',
        end_date: '2024-11-01',
        group_by: 'day',
    })

    const { data: weatherData } = useQuery(WeatherRawQueries.weatherDateRangeQuery(filter))

    return (
        <Pattern1Provider value={{ weatherData, groupBy, filter }}>
            <WeatherDashboardControls />
            <div className='flex flex-col gap-4'>
                <WeatherLineChart dataType='avg_temp_c' title='Average Temperature C degree' color='red'/>
                <WeatherLineChart dataType='avg_gust_kph' title='Average Gust KPH' color='blue' />
                <WeatherLineChart dataType='avg_humidity' title='Average Humidity' color='green' />
                <WeatherLineChart dataType='avg_precip_mm' title='Average Precipitation mm' color='yellow' />
                <WeatherLineChart dataType='avg_wind_kph' title='Average Wind KPH' color='purple' />
                <WeatherLineChart dataType='avg_windchill_c' title='Average Wind Chill C degree' color='orange' />
                <WeatherLineChart dataType='avg_feelslike_c' title='Average Feels Like C degree' color='pink' />
            </div>
        </Pattern1Provider>
    )
}

export default Pattern1Dashboard