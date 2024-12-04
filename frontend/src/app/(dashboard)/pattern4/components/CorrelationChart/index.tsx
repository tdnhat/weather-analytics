import React from "react";
import Plot from "react-plotly.js";
import { usePattern4Context } from '../Pattern4Dashboard/context';

const CorrelationChart = () => {
  const { correlationData } = usePattern4Context();

  if (!correlationData) {
    return <div>Không có dữ liệu tương quan</div>;
  }

  // Access the first data point
  const dataPoint = correlationData[0];

  const labels = ["Nhiệt độ", "Độ ẩm", "Áp suất", "Gió"];
  const matrix = [
    [1, dataPoint.temp_humidity_corr, dataPoint.temp_pressure_corr, dataPoint.temp_wind_corr],
    [dataPoint.humidity_temp_corr, 1, dataPoint.humidity_pressure_corr, dataPoint.humidity_wind_corr],
    [dataPoint.pressure_temp_corr, dataPoint.pressure_humidity_corr, 1, dataPoint.pressure_wind_corr],
    [dataPoint.wind_temp_corr, dataPoint.wind_humidity_corr, dataPoint.wind_pressure_corr, 1],
  ];

  return (
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
        title: "Biểu đồ ma trận tương quan",
        xaxis: { side: "bottom" },
        margin: { l: 50, r: 50, t: 50, b: 50 },
      }}
      config={{ responsive: true }}
      style={{ width: "100%", height: "100%" }}
    />
  );
};

export default CorrelationChart;
