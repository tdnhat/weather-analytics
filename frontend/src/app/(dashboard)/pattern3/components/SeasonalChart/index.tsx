import { useMemo } from "react";
import { usePattern3Context } from "../Pattern3Dashboard/context";
import Plot from "react-plotly.js";

interface IProps {
    dataType: 'avg_temp' | 'avg_humidity' | 'total_precip' | 'avg_wind' | 'avg_pressure',
    title: string,
    yAxisTitle: string
}

function SeasonalChart({ dataType, title, yAxisTitle }: IProps) {
    const { seasonalData } = usePattern3Context();

    const plotData = useMemo(() => {
        const quarterData: { [key: number]: { dates: string[], values: number[] } } = {};
        
        if (seasonalData?.data?.data && Array.isArray(seasonalData.data.data)) {
            seasonalData.data.data.forEach(item => {
                if (!quarterData[item.quarter]) {
                    quarterData[item.quarter] = { dates: [], values: [] };
                }
                quarterData[item.quarter].dates.push(item.date);
                quarterData[item.quarter].values.push(item[dataType]);
            });
        }

        return Object.entries(quarterData).map(([quarter, data]) => ({
            x: data.dates,
            y: data.values,
            type: 'scatter',
            mode: 'lines',
            name: `Q${quarter}`,
        }));
    }, [seasonalData, dataType]);

    if (!plotData.length) {
        return <div>No data available</div>;
    }

    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96c93d'];

    return (
        <Plot
            className='w-full'
            data={plotData.map((trace, index) => ({
                ...trace,
                line: { 
                    color: colors[index % colors.length],
                    width: 1.5
                }
            }))}
            layout={{
                autosize: true,
                height: 400,
                title: {
                    text: title,
                    font: { 
                        size: 16,
                        color: '#2d3436'
                    }
                },
                margin: { l: 50, r: 20, t: 40, b: 50 },
                xaxis: {
                    title: 'Date',
                    tickangle: 45,
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false
                },
                yaxis: {
                    title: yAxisTitle,
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false
                },
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                showlegend: true,
                legend: {
                    x: 1,
                    xanchor: 'right',
                    y: 1
                },
                hovermode: 'x unified'
            }}
            useResizeHandler
            style={{ width: '100%' }}
            config={{
                displayModeBar: false
            }}
        />
    );
}

export default SeasonalChart; 