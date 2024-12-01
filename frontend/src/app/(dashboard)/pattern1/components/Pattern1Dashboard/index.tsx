import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawQueries } from '@/entities/weatherRaw/queries'
import { Pattern1Provider } from './context'
import WeatherLineChart from '../WeatherLineChart/index'

interface IProps {
    groupBy?: 'day' | 'month' | 'week';
    filter?: {
        start_date: string;
        end_date: string;
        group_by: 'day' | 'month' | 'week';
    };
}

const defaultStartDate = '2023-11-20';
const defaultEndDate = new Date().toISOString().split('T')[0]; //yyyy-mm-dd

function Pattern1Dashboard({ filter = { start_date: defaultStartDate, end_date: defaultEndDate, group_by: 'day'} }: IProps) {
    const { data: dailyData } = useQuery(
        WeatherRawQueries.weatherDateRangeQuery({
            ...filter,
            group_by: 'day'
        })
    )

    const { data: weeklyData } = useQuery(
        WeatherRawQueries.weatherDateRangeQuery({
            ...filter,
            group_by: 'week'
        })
    )

    const { data: monthlyData } = useQuery(
        WeatherRawQueries.weatherDateRangeQuery({
            ...filter,
            group_by: 'month'
        })
    )

    return (
        <div className='flex flex-col gap-8'>
            <section>
                <h2 className='text-xl font-bold mb-4'>Daily Weather Trends</h2>
                <Pattern1Provider value={{ weatherData: dailyData, groupBy: 'day', filter }}>
                    <div className='flex flex-col gap-4'>
                        <WeatherLineChart dataType='avg_temp_c' title={`Daily Average Temperature (${dailyData?.start_date} - ${dailyData?.end_date})`} color='red'/>
                    </div>
                </Pattern1Provider>
            </section>

            <section>
                <h2 className='text-xl font-bold mb-4'>Weekly Weather Trends</h2>
                <Pattern1Provider value={{ weatherData: weeklyData, groupBy: 'week', filter }}>
                    <div className='flex flex-col gap-4'>
                        <WeatherLineChart dataType='avg_temp_c' title={`Weekly Average Temperature (Week 47/2023 - Week 47/2024)`} color='blue'/>
                    </div>
                </Pattern1Provider>
            </section>

            <section>
                <h2 className='text-xl font-bold mb-4'>Monthly Weather Trends</h2>
                <Pattern1Provider value={{ weatherData: monthlyData, groupBy: 'month', filter }}>
                    <div className='flex flex-col gap-4'>
                        <WeatherLineChart dataType='avg_temp_c' title={`Monthly Average Temperature (11/2023 - 11/2024)`} color='green'/>
                    </div>
                </Pattern1Provider>
            </section>
        </div>
    )
}

export default Pattern1Dashboard