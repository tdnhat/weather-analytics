import { z } from 'zod'
import { 
    QueryParamsWeatherDateRangeDtoSchema,
    WeatherDateRangeResponseDtoSchema
} from './contracts'

export type QueryParamsWeatherDateRangeDto = z.infer<typeof QueryParamsWeatherDateRangeDtoSchema>
export type WeatherDateRangeResponseDto = z.infer<typeof WeatherDateRangeResponseDtoSchema>
