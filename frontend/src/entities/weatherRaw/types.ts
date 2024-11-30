import { z } from 'zod'
import { QueryParamsWeatherDateRangeSchema } from './contracts'

export type QueryParamsWeatherDateRange = z.infer<typeof QueryParamsWeatherDateRangeSchema>