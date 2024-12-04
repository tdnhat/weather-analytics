import React, { useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawService } from '@/api/weather/service'
import WeatherTrendChart from '../WeatherTrendChart'
import SeasonalChart from '../SeasonalChart'
import CorrelationChart from '../CorrelationChart'

const defaultStartDate = '2023-11-20';
const defaultEndDate = new Date().toISOString().split('T')[0];
const defaultQuarters = [1, 2, 3, 4];

function AnalysisDashboard() {
    const containerRef = useRef<HTMLDivElement>(null);

    const { data: dailyTrends } = useQuery({
        queryKey: ['daily-trends'],
        queryFn: () => WeatherRawService.getDailyTrends({ 
            params: { 
                start_date: defaultStartDate,
                end_date: defaultEndDate
            } 
        })
    })

    const { data: seasonalData } = useQuery({
        queryKey: ['seasonal-data'],
        queryFn: () => WeatherRawService.getSeasonalData({ 
            params: { 
                start_date: defaultStartDate,
                end_date: defaultEndDate,
                quarters: defaultQuarters
            } 
        })
    })

    const { data: correlationData } = useQuery({
        queryKey: ['correlation'],
        queryFn: () => WeatherRawService.getCorrelation({ 
            params: { year: 2023 } 
        })
    })

    if (!dailyTrends || !seasonalData || !correlationData) {
        return <div>Loading...</div>
    }

    return (
        <div ref={containerRef} className='grid grid-cols-10 gap-6'>
            {/* Seasonal Analysis */}
            <div className='col-span-10'>
                <h2 className='text-xl font-bold mb-4'>Biểu đồ nhiệt độ theo quý</h2>
                <div className='bg-white rounded-lg p-4 shadow-sm'>
                    <SeasonalChart 
                        dataType='avg_temp'
                        title='Biểu đồ nhiệt độ theo quý'
                        yAxisTitle='Nhiệt độ (°C)'
                        data={seasonalData?.data}
                    />
                </div>
            </div>

            {/* Moving Average Analysis */}
            <div className='col-span-7'>
                <h2 className='text-xl font-bold mb-4'>Biểu đồ trend của nhiệt độ</h2>
                <div className='bg-white rounded-lg p-4 shadow-sm'>
                    <WeatherTrendChart 
                        dataType='avg_temp'
                        title='Biểu đồ trend của nhiệt độ'
                        yAxisTitle='Nhiệt độ (°C)'
                        data={dailyTrends?.data}
                    />
                </div>
            </div>

            {/* Correlation Analysis */}
            <div className='col-span-3'>
                <h2 className='text-xl font-bold mb-4'>Biểu đồ tương quan nhiệt độ</h2>
                <div className='bg-white rounded-lg p-4 shadow-sm'>
                    <CorrelationChart data={correlationData?.data?.data} />
                </div>
            </div>
        </div>
    )
}

export default AnalysisDashboard