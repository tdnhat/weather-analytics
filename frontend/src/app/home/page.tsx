import TemperatureDecomposition from "@/components/TemperatureDecomposition";
import WeatherCharts from "@/components/WeatherCharts";
import TemperatureDistribution from "@/components/TemperatureDistribution";
import TemperatureCorrelation from "@/components/TemperatureCorrelation";
export default function Home() {
    return (
        <main className="max-w-screen-xl flex flex-col mx-auto p-4 gap-8">
            <WeatherCharts />
            <TemperatureDistribution />
            <TemperatureDecomposition />
        </main>
    )
}