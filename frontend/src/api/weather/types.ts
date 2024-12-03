import { z } from 'zod'
import { 
    QueryParamsWeatherDateRangeDtoSchema,
    WeatherDateRangeResponseDtoSchema,
    CorrelationResponseSchema,
    CorrelationDataSchema,
    CorrelationQueryParamsSchema,
    DailyTrendsResponseSchema,
    DailyTrendsDataSchema,
    DailyTrendsQueryParamsSchema,
    SeasonalDataDataSchema,
    SeasonalDataQueryParamsSchema,
    SeasonalDataResponseSchema
} from './contracts'

export type QueryParamsWeatherDateRangeDto = z.infer<typeof QueryParamsWeatherDateRangeDtoSchema>
export type WeatherDateRangeResponseDto = z.infer<typeof WeatherDateRangeResponseDtoSchema>

export type CorrelationResponse = z.infer<typeof CorrelationResponseSchema>
export type CorrelationData = z.infer<typeof CorrelationDataSchema>
export type CorrelationQueryParams = z.infer<typeof CorrelationQueryParamsSchema>

export type DailyTrendsResponse = z.infer<typeof DailyTrendsResponseSchema>
export type DailyTrendsData = z.infer<typeof DailyTrendsDataSchema>
export type DailyTrendsQueryParams = z.infer<typeof DailyTrendsQueryParamsSchema>

export type SeasonalDataResponse = z.infer<typeof SeasonalDataResponseSchema>
export type SeasonalDataData = z.infer<typeof SeasonalDataDataSchema>
export type SeasonalDataQueryParams = z.infer<typeof SeasonalDataQueryParamsSchema>
