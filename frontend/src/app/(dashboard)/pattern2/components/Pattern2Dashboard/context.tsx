import { createContext, useContext } from "react"

interface DailyData {
    data: {
        data: Array<{
            date: string;
            avg_temp: number;
            avg_humidity: number;
            total_precip: number;
            avg_wind: number;
            avg_pressure?: number;
        }>;
    };
}

interface IPattern2ContextProps {
    correlationData?: DailyData;
}

export const Pattern2Context = createContext<IPattern2ContextProps>({
    correlationData: undefined
})

export const Pattern2Provider = Pattern2Context.Provider

export const usePattern2Context = () => {
    return useContext(Pattern2Context)
}
