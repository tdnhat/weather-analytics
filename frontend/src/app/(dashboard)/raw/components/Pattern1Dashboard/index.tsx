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
                <h2 className='text-xl font-bold mb-4 text-white'>Biểu đồ nhiệt độ trung bình hằng ngày</h2>
                <div className='bg-white rounded-lg p-6'>
                    <Pattern1Provider value={{ weatherData: dailyData, groupBy: 'day', filter }}>
                        <WeatherLineChart dataType='avg_temp_c' title={`Nhiệt độ trung bình hằng ngày (${dailyData?.start_date} - ${dailyData?.end_date})`} color='red'/>
                    </Pattern1Provider>
                </div>
            </section>

            <section>
                <h2 className='text-xl font-bold mb-4 text-white'>Biểu đồ nhiệt độ trung bình hằng tuần</h2>
                <div className='bg-white rounded-lg p-6'>
                    <Pattern1Provider value={{ weatherData: weeklyData, groupBy: 'week', filter }}>
                        <WeatherLineChart dataType='avg_temp_c' title={`Nhiệt độ trung bình hằng tuần (Tuần 47/2023 - Tuần 47/2024)`} color='#60a5fa'/>
                    </Pattern1Provider>
                </div>
            </section>

            <section>
                <h2 className='text-xl font-bold mb-4 text-white'>Biểu đồ nhiệt độ trung bình hằng tháng</h2>
                <div className='bg-white rounded-lg p-6'>
                    <Pattern1Provider value={{ weatherData: monthlyData, groupBy: 'month', filter }}>
                        <WeatherLineChart dataType='avg_temp_c' title={`Nhiệt độ trung bình hằng tháng (11/2023 - 11/2024)`} color='#22c55e'/>
                    </Pattern1Provider>
                </div>
            </section>
        </div>
    )
}

export default Pattern1Dashboard