import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawService } from '@/api/weather/service'
import { Pattern2Provider } from './context'
import WeatherTrendChart from '../WeatherTrendChart'

interface IProps {
    filter?: {
        start_date: string;
        end_date: string;
    };
}

const defaultStartDate = '2023-11-20';
const defaultEndDate = new Date().toISOString().split('T')[0]; //yyyy-mm-dd

function Pattern2Dashboard({ filter = { start_date: defaultStartDate, end_date: defaultEndDate } }: IProps) {
    const { data: dailyData, error, isLoading } = useQuery({
        queryKey: ['daily-trends'],
        queryFn: () => WeatherRawService.getDailyTrends({ 
            params: { 
                start_date: filter.start_date,
                end_date: filter.end_date
            } 
        })
    })

    if (isLoading) return <div>Loading...</div>
    if (error) return <div>Error loading data</div>

    return (
        <div className='flex flex-col gap-8'>
            <section>
                <h2 className='text-xl font-bold mb-4'>Weather Trends Analysis</h2>
                <Pattern2Provider value={{ correlationData: dailyData }}>
                    <div className='w-full'>
                        <WeatherTrendChart 
                            dataType='avg_temp'
                            title='Temperature Trend'
                            color='red'
                            yAxisTitle='Temperature (°C)'
                        />
                    </div>
                </Pattern2Provider>
            </section>
        </div>
    )
}

export default Pattern2Dashboard