import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawService } from '@/api/weather/service'
import { Pattern3Provider } from './context'
import SeasonalChart from '../SeasonalChart'

interface IProps {
    filter?: {
        start_date: string;
        end_date: string;
        quarters?: number[];
    };
}

const defaultStartDate = '2023-11-20';
const defaultEndDate = new Date().toISOString().split('T')[0];
const defaultQuarters = [1, 2, 3, 4];

function Pattern3Dashboard({ 
    filter = { 
        start_date: defaultStartDate, 
        end_date: defaultEndDate,
        quarters: defaultQuarters 
    } 
}: IProps) {
    const { data: seasonalData, error, isLoading } = useQuery({
        queryKey: ['seasonal-data', filter],
        queryFn: () => WeatherRawService.getSeasonalData({ 
            params: { 
                start_date: filter.start_date,
                end_date: filter.end_date,
                quarters: filter.quarters
            } 
        })
    })

    if (isLoading) return <div>Loading...</div>
    if (error) return <div>Error loading data</div>

    return (
        <div className='flex flex-col gap-8'>
            <section>
                <h2 className='text-xl font-bold mb-4'>Biểu đồ nhiệt độ theo quý</h2>
                <Pattern3Provider value={{ seasonalData }}>
                    <div className='w-full'>
                        <SeasonalChart 
                            dataType='avg_temp'
                            title='Nhiệt độ trung bình'
                            yAxisTitle='Nhiệt độ (°C)'
                        />
                    </div>
                </Pattern3Provider>
            </section>
        </div>
    )
}

export default Pattern3Dashboard
