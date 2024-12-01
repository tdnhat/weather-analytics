import { z } from 'zod'
import { 
    QueryParamsWeatherDateRangeDtoSchema,
    WeatherDateRangeResponseDtoSchema,
    CorrelationResponseSchema,
    CorrelationDataSchema,
    CorrelationQueryParamsSchema
} from './contracts'

export type QueryParamsWeatherDateRangeDto = z.infer<typeof QueryParamsWeatherDateRangeDtoSchema>
export type WeatherDateRangeResponseDto = z.infer<typeof WeatherDateRangeResponseDtoSchema>

export type CorrelationResponse = z.infer<typeof CorrelationResponseSchema>
export type CorrelationData = z.infer<typeof CorrelationDataSchema>
export type CorrelationQueryParams = z.infer<typeof CorrelationQueryParamsSchema>
