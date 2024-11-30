import { z } from 'zod'

export const QueryParamsWeatherDateRangeSchema = z.object({
    start_date: z.string(),
    end_date: z.string(),
    group_by: z.enum(['day', 'month', 'week']),
})
