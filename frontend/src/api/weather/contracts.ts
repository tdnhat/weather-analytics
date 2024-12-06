import { z } from 'zod'

const WeatherDateRangeSchema = z.object({
    avg_temp_c: z.number(),
    avg_wind_kph: z.number(),
    avg_humidity: z.number(),
    avg_precip_mm: z.number(),
    avg_gust_kph: z.number(),
    avg_feelslike_c: z.number(),
    avg_windchill_c: z.number(),
})

const MonthlyWeatherSchema = WeatherDateRangeSchema.extend({
    year: z.number().int(),
    month: z.number().int().min(1).max(12),
}).describe('MonthlyWeatherSchema')

const WeeklyWeatherSchema = WeatherDateRangeSchema.extend({
    year: z.number().int(),
    week: z.number().int().min(1),
}).describe('WeeklyWeatherSchema')

const DailyWeatherSchema = WeatherDateRangeSchema.extend({
    year: z.number().int(),
    month: z.number().int().min(1).max(12),
    day: z.number().int().min(1).max(31),
}).describe('DailyWeatherSchema')

// Request Dto
export const QueryParamsWeatherDateRangeDtoSchema = z.object({
    start_date: z.string(),
    end_date: z.string(),
    group_by: z.enum(['day', 'month', 'week']),
})

// Response Dto
export const WeatherDateRangeResponseDtoSchema = z.object({
    start_date: z.string(),
    end_date: z.string(),
    group_by: z.enum(['day', 'month', 'week']),
    data: z.array(DailyWeatherSchema.or(MonthlyWeatherSchema).or(WeeklyWeatherSchema)),
})

export const CorrelationDataSchema = z.object({
    date: z.string(),
    temp_humidity_corr: z.number(),
    temp_pressure_corr: z.number(),
    temp_wind_corr: z.number(),
    humidity_temp_corr: z.number(),
    humidity_pressure_corr: z.number(),
    humidity_wind_corr: z.number(),
    pressure_temp_corr: z.number(),
    pressure_humidity_corr: z.number(),
    pressure_wind_corr: z.number(),
    wind_temp_corr: z.number(),
    wind_humidity_corr: z.number(),
    wind_pressure_corr: z.number(),
})

export const CorrelationResponseSchema = z.object({
    data: z.array(CorrelationDataSchema)
})

export const CorrelationQueryParamsSchema = z.object({
    year: z.number()
})

export const DailyTrendsDataSchema = z.object({
    date: z.string(),
    avg_temp: z.number(),
    avg_humidity: z.number(),
    total_precip: z.number(),
    avg_wind: z.number(),
})

export const DailyTrendsQueryParamsSchema = z.object({
    start_date: z.string(),
    end_date: z.string(),
})

export const DailyTrendsResponseSchema = z.object({
    data: z.array(DailyTrendsDataSchema)
})

export const SeasonalDataDataSchema = z.object({
    year: z.number().int(),
    quarter: z.number().int().min(1).max(4),
    avg_temp: z.number(),
    avg_humidity: z.number(),
})

export const SeasonalDataQueryParamsSchema = z.object({
    start_date: z.string(),
    end_date: z.string(),
    quarters: z.array(z.number().int().min(1).max(4))
})

export const SeasonalDataResponseSchema = z.object({
    data: z.array(SeasonalDataDataSchema)
})

export const SpiderChartDataSchema = z.object({
    id: z.number(),
    year: z.number(),
    summer_quantity: z.number(),
    winter_quantity: z.number(),
    autumn_quantity: z.number(), 
    spring_quantity: z.number()
})

export const SpiderChartQueryParamsSchema = z.object({
    year: z.number()
})

export const SpiderChartResponseSchema = z.object({
    data: z.array(SpiderChartDataSchema)
})
