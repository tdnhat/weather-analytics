import { createContext, useContext } from "react"

interface SeasonalData {
    year: number;
    quarter: number;
    avg_temp: number;
    avg_humidity: number;
    date?: string;
    total_precip?: number;
    avg_wind?: number;
    avg_pressure?: number;
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
