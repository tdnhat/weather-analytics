import { httpGet } from '@/api/axios'
import { QueryParamsWeatherDateRangeDto, WeatherDateRangeResponseDto } from './types'

export class WeatherRawService {
    static weatherDateRangeQuery(config: {
        params: QueryParamsWeatherDateRangeDto
    }) {
        return httpGet<WeatherDateRangeResponseDto>('/weather-raw/date-range', config)
    }
}