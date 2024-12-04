import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawService } from '@/api/weather/service'
import { Pattern4Provider } from './context'
import CorrelationChart from '../CorrelationChart'

function Pattern4Dashboard() {
    const { data: correlationData, error, isLoading } = useQuery({
        queryKey: ['correlation'],
        queryFn: () => WeatherRawService.getCorrelation({ params: { year: 2023 } })
    })

    if (isLoading) return <div>Loading...</div>
    if (error) return <div>Error loading data</div>
    return (
        <div className='flex flex-col gap-8'>
            <section>
                <h2 className='text-xl font-bold mb-4'>Biểu đồ ma trận tương quan</h2>
                <Pattern4Provider value={{ correlationData: correlationData?.data?.data ?? [] }}>
                    <div className='flex flex-col gap-4'>
                        <CorrelationChart />
                    </div>
                </Pattern4Provider>
            </section>
        </div>
    )
}

export default Pattern4Dashboard