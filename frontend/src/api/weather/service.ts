import { httpGet } from '@/api/axios'
import { 
    QueryParamsWeatherDateRangeDto, 
    WeatherDateRangeResponseDto,
    CorrelationQueryParams,
    CorrelationResponse,
    DailyTrendsQueryParams,
    DailyTrendsResponse
} from './types'

export class WeatherRawService {
    static weatherDateRangeQuery(config: {
        params: QueryParamsWeatherDateRangeDto
    }) {
        return httpGet<WeatherDateRangeResponseDto>('/weather-raw/date-range', config)
    }

    static getCorrelation(config: {
        params: CorrelationQueryParams
    }) {
        return httpGet<CorrelationResponse>('/analysis/correlation', config)
    }

    static getDailyTrends(config: {
        params: DailyTrendsQueryParams
    }) {
        return httpGet<DailyTrendsResponse>('/analysis/daily', config)
    }
}