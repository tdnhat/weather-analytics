import { WeatherRawService } from '@/api/weather'
import { queryOptions } from '@tanstack/react-query'
import { QueryParamsWeatherDateRange } from './types'

export class WeatherRawQueries {
    static keys = {
        root: ['weather-raw'] as const,
    }

    static weatherDateRangeQuery(params: QueryParamsWeatherDateRange) {
        const { start_date, end_date, group_by } = params

        const queryKey = [
            ...this.keys.root,
            'date-range',
            { start_date },
            { end_date },
            { group_by },
        ]

        return queryOptions({
            queryKey,
            queryFn: async () => {
                const response = await WeatherRawService.weatherDateRangeQuery({
                    params,
                })

                return response.data
            },
        })
    }
}
