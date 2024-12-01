import { createContext, useContext } from "react"
import { weatherRawTypesDto } from "@/api/weather"

interface IPattern4ContextProps {
    correlationData?: weatherRawTypesDto.CorrelationResponse
}

export const Pattern4Context = createContext<IPattern4ContextProps>({
    correlationData: undefined
})

export const Pattern4Provider = Pattern4Context.Provider


export const usePattern4Context = () => {
    return useContext(Pattern4Context)
}
