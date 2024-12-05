import { useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { SpiderChartData } from "@/api/weather/types";

interface IProps {
    data: SpiderChartData;
}

function SpiderChart({ data }: IProps) {
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

    // Calculate percentages for each season
    const total = data.spring_quantity + data.summer_quantity + 
                 data.autumn_quantity + data.winter_quantity;
    
    const getPercentage = (value: number) => ((value / total) * 100).toFixed(1);

    const values = [
        data.spring_quantity, // 0 o'clock
        data.summer_quantity, // 3 o'clock
        data.autumn_quantity, // 6 o'clock
        data.winter_quantity, // 9 o'clock
        data.spring_quantity, // Repeated to close the polygon
    ];

    const labels = ['Xuân', 'Hạ', 'Thu', 'Đông', 'Xuân'];
    const percentages = values.map(v => getPercentage(v));

    // Custom hover text
    const hovertext = values.map((value, index) => {
        if (index === values.length - 1) return ''; // Skip the repeated point
        return `Mùa ${labels[index]}:<br>` +
               `${value} ngày<br>` +
               `${percentages[index]}%`;
    });

    return (
        <div ref={chartRef} className="w-full">
            <Plot
                data={[
                    {
                        type: 'scatterpolar',
                        r: values,
                        theta: labels,
                        fill: 'toself',
                        name: `Năm ${data.year}`,
                        line: {
                            color: '#0ea5e9',
                            width: 2,
                        },
                        fillcolor: 'rgba(14, 165, 233, 0.2)',
                        hoverinfo: 'text',
                        hovertext: hovertext,
                        hoverlabel: {
                            bgcolor: '#fff',
                            bordercolor: '#0ea5e9',
                            font: { family: 'Arial', size: 12 }
                        }
                    }
                ]}
                layout={{
                    width: containerWidth,
                    height: 500, // Increased height
                    polar: {
                        radialaxis: {
                            visible: true,
                            range: [0, Math.max(...values) + 5],
                            title: {
                                text: 'Số ngày',
                                font: { size: 12, color: '#0e7490' }
                            },
                            tickfont: { color: '#0e7490' },
                            gridcolor: '#e2e8f0',
                            linecolor: '#e2e8f0'
                        },
                        angularaxis: {
                            tickfont: { color: '#0e7490', size: 12 },
                            linecolor: '#e2e8f0',
                            gridcolor: '#e2e8f0'
                        },
                        bgcolor: 'rgba(255,255,255,0.9)'
                    },
                    showlegend: true,
                    legend: {
                        x: 1.1, // Moved to the right
                        y: 0.5, // Centered vertically
                        xanchor: 'left',
                        yanchor: 'middle',
                        orientation: 'v',
                        font: { color: '#0e7490', size: 14 }
                    },
                    title: {
                        text: `Phân bố theo mùa`,
                        font: { size: 16, color: '#0e7490' },
                    },
                    margin: { t: 50, b: 50, l: 50, r: 100 }, // Increased right margin for legend
                    paper_bgcolor: 'white',
                    plot_bgcolor: 'white',
                }}
                config={{
                    responsive: true,
                    displayModeBar: false,
                    displaylogo: false,
                }}
            />
        </div>
    );
}

export default SpiderChart;