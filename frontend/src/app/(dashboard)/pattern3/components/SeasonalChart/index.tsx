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
        const quarterlyData: { [key: string]: { dates: string[], values: number[], quarter: number } } = {};
        
        if (seasonalData?.data?.data && Array.isArray(seasonalData.data.data)) {
            seasonalData.data.data.forEach(item => {
                const key = `${item.year}-Q${item.quarter}`;
                if (!quarterlyData[key]) {
                    quarterlyData[key] = { dates: [], values: [], quarter: item.quarter };
                }
                quarterlyData[key].dates.push(item.date || '');
                quarterlyData[key].values.push(item[dataType] || 0);
            });
        }

        const quarterColors = {
            1: '#7bc86c',  // soft green
            2: '#f5d76e',  // soft yellow
            3: '#ffb366',  // soft orange
            4: '#85c1e9'   // soft blue
        };

        return Object.entries(quarterlyData).map(([key, data]) => ({
            x: data.dates,
            y: data.values,
            type: 'scatter',
            mode: 'lines+markers',
            name: key,
            line: {
                shape: 'spline',
                width: 2,
                color: quarterColors[data.quarter as keyof typeof quarterColors]
            },
            marker: {
                size: 6,
                opacity: 0.7
            }
        }));
    }, [seasonalData, dataType]);

    if (!plotData.length) {
        return <div>No data available</div>;
    }

    return (
        <Plot
            className='w-full'
            data={plotData as any}
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
                    zeroline: false,
                    showspikes: true,
                    spikemode: 'across',
                    spikethickness: 1
                },
                yaxis: {
                    title: yAxisTitle,
                    tickfont: { size: 11 },
                    showgrid: true,
                    gridcolor: '#f5f6fa',
                    zeroline: false,
                    showspikes: true,
                    spikethickness: 1
                },
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                showlegend: true,
                legend: {
                    x: 1,
                    xanchor: 'right',
                    y: 1,
                    bgcolor: 'rgba(255, 255, 255, 0.8)',
                    bordercolor: '#f5f6fa',
                    borderwidth: 1
                },
                hovermode: 'x unified',
                modebar: {
                    remove: ['autoScale2d', 'lasso2d', 'pan2d', 'select2d', 'toggleSpikelines', 'hoverClosestCartesian'],
                    add: ['hoverclosest']
                },
            }}
            config={{
                responsive: true
            }}
        />
    );
}

export default SeasonalChart; 