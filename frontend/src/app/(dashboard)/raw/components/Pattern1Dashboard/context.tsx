import { createContext, useContext } from "react"
import { weatherRawTypesDto } from "@/api/weather"

interface IPattern1ContextProps {
    weatherData?: weatherRawTypesDto.WeatherDateRangeResponseDto
    groupBy?: 'day' | 'month' | 'week',
    filter: {start_date: string, end_date: string, group_by: 'day' | 'month' | 'week'}
}

export const Pattern1Context = createContext<IPattern1ContextProps>({
    weatherData: undefined,
    groupBy: 'day',
    filter: {start_date: '', end_date: '', group_by: 'day'}
})

export const Pattern1Provider = Pattern1Context.Provider


export const usePattern1Context = () => {
    return useContext(Pattern1Context)
}
