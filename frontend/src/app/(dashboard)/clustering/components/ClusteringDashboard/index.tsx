import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { WeatherRawService } from '@/api/weather/service'
import SpiderChart from '../SpiderChart'
import SeasonProbability from '../SeasonProbability'

function ClusteringDashboard() {
    const { data: spiderData, isError, isLoading } = useQuery({
        queryKey: ['spider-chart'],
        queryFn: () => WeatherRawService.getSpiderChart({ 
            params: { year: 2024 } 
        })
    })

    return (
        <div className='grid grid-cols-10 gap-6'>
            <div className='col-span-10 lg:col-span-5'>
                <h2 className='text-xl font-bold mb-4 text-white'>Phân bố theo mùa</h2>
                <div className='bg-white rounded-lg p-6 h-[600px] relative'>
                    {isLoading && (
                        <div className='absolute inset-0 flex items-center justify-center bg-white bg-opacity-75'>
                            <div className='animate-spin rounded-full h-8 w-8 border-b-2 border-sky-500'></div>
                        </div>
                    )}
                    
                    {isError && (
                        <div className='absolute inset-0 flex items-center justify-center'>
                            <div className='text-red-500'>
                                Đã có lỗi xảy ra khi tải dữ liệu
                            </div>
                        </div>
                    )}

                    {!isLoading && !isError && spiderData && (
                        <SpiderChart data={spiderData.data} />
                    )}
                </div>
            </div>

            <div className='col-span-10 lg:col-span-5'>
                <h2 className='text-xl font-bold mb-4 text-white'>Xác suất phân mùa</h2>
                <div className='bg-white rounded-lg p-6 h-[600px]'>
                    <SeasonProbability />
                </div>
            </div>
        </div>
    )
}

export default ClusteringDashboard