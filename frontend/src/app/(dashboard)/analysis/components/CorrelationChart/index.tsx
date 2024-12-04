import { useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";

interface IProps {
    data: any[] // Type this according to your correlation data structure
}

function CorrelationChart({ data }: IProps) {
    const chartRef = useRef<HTMLDivElement>(null);
    const [containerWidth, setContainerWidth] = useState(0);

    useEffect(() => {
        const updateWidth = () => {
            if (chartRef.current) {
                setContainerWidth(chartRef.current.clientWidth);
            }
        };

        const resizeObserver = new ResizeObserver(updateWidth);
        if (chartRef.current) {
            resizeObserver.observe(chartRef.current);
        }

        return () => resizeObserver.disconnect();
    }, []);

    if (!data || data.length === 0) {
        return <div>No correlation data available</div>;
    }

    const dataPoint = data[0];
    const labels = ["Nhiệt độ", "Độ ẩm", "Áp suất", "Gió"];
    const matrix = [
        [1, dataPoint.temp_humidity_corr, dataPoint.temp_pressure_corr, dataPoint.temp_wind_corr],
        [dataPoint.humidity_temp_corr, 1, dataPoint.humidity_pressure_corr, dataPoint.humidity_wind_corr],
        [dataPoint.pressure_temp_corr, dataPoint.pressure_humidity_corr, 1, dataPoint.pressure_wind_corr],
        [dataPoint.wind_temp_corr, dataPoint.wind_humidity_corr, dataPoint.wind_pressure_corr, 1],
    ];

    return (
        <div ref={chartRef} className="w-full">
            <Plot
                data={[
                    {
                        z: matrix,
                        x: labels,
                        y: labels,
                        type: "heatmap",
                        colorscale: "Viridis",
                        text: matrix.map(row => 
                            row.map(value => value.toFixed(2))
                        ),
                        texttemplate: "%{text}",
                        textfont: { color: "white" },
                        hoverongaps: false,
                    },
                ]}
                layout={{
                    width: containerWidth,
                    height: 400,
                    title: {
                        text: "Ma trận tương quan",
                        font: { size: 16 }
                    },
                    margin: { l: 50, r: 50, t: 50, b: 50 },
                    xaxis: { side: "bottom" },
                }}
                config={{
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                }}
            />
        </div>
    );
}

export default CorrelationChart;