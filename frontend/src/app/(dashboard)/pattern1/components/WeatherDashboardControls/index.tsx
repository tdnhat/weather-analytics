import { z } from 'zod'
import React from 'react'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from '@/ui/Button'
import { Input } from '@/ui/Input'
import { useForm } from 'react-hook-form'

const formSchema = z.object({
    start_date: z.string().datetime(),
    end_date: z.string().datetime(),
    group_by: z.enum(['day', 'week', 'month']),
})

type FormValues = z.infer<typeof formSchema>

function WeatherDashboardControls() {
    const { register, handleSubmit, formState: {errors} } = useForm<FormValues>({
        resolver: zodResolver(formSchema),
    })

    const onSubmit = (data: any) => {
        console.log(data)
    }

    return (
        <div className='w-full'>
            <form onSubmit={handleSubmit(onSubmit)} className='grid grid-cols-3 gap-4'>
                <div className='relative'>
                    <label htmlFor='start_date' className='text-sm font-medium'>Start Date</label>
                    <Input {...register('start_date')} />
                    {errors.start_date && <p className='block absolute -bottom-[20px] text-red-500 text-sm'>{errors.start_date.message}</p>}
                </div>
                <div className='relative'>
                    <label htmlFor='end_date' className='text-sm font-medium'>End Date</label>
                    <Input {...register('end_date')} />
                    {errors.end_date && <p className='block absolute -bottom-[20px] text-red-500 text-sm'>{errors.end_date.message}</p>}
                </div>
                <div>
                    <label htmlFor='group_by' className='text-sm font-medium'>Group By</label>
                    <Input {...register('group_by')} />
                </div>
                <div className='col-span-3 flex justify-center'>
                    <Button variant='default' type='submit' className='w-1/2 bg-blue-500 text-white hover:bg-blue-600'>Update</Button>
                </div>
            </form>
        </div>
    )
}

export default WeatherDashboardControls