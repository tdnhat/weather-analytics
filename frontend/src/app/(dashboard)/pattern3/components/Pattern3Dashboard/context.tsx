import { createContext, useContext } from "react"

interface SeasonalData {
    date: string;
    year: number;
    quarter: number;
    avg_temp: number;
    avg_humidity: number;
    total_precip: number;
    avg_wind: number;
    avg_pressure: number;
    max_temp: number;
    min_temp: number;
}

interface IPattern3ContextProps {
    seasonalData?: {
        data: {
            data: SeasonalData[];
        };
    };
}

export const Pattern3Context = createContext<IPattern3ContextProps>({
    seasonalData: undefined
})

export const Pattern3Provider = Pattern3Context.Provider

export const usePattern3Context = () => {
    return useContext(Pattern3Context)
}
