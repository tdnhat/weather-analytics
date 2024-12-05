'use client'

import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface PredictionData {
    predicted_temperature: number;
    predicted_humidity: number;
    predicted_pressure: number;
}

function PredictionPage() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const formattedDate = tomorrow.toISOString().split('T')[0];

    const { data } = useQuery({
        queryKey: ['prediction', formattedDate],
        queryFn: async () => {
            const response = await axios.get<PredictionData>(
                `http://localhost:8000/api/prediction/tomorrow?date=${formattedDate}`
            );
            return response.data;
        }
    });

    return (
        <div className="w-full h-full p-4">
            <div className="bg-white rounded-lg p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-cyan-700 mb-6">
                    Dự báo thời tiết ngày mai
            </h2>
            
            {data && (
                <div className="space-y-4">
                    <div className="flex items-center">
                        <span className="w-32 text-cyan-700">Nhiệt độ:</span>
                        <span className="font-medium">
                            {data.predicted_temperature.toFixed(1)}°C
                        </span>
                    </div>
                    <div className="flex items-center">
                        <span className="w-32 text-cyan-700">Độ ẩm:</span>
                        <span className="font-medium">
                            {data.predicted_humidity.toFixed(1)}%
                        </span>
                    </div>
                    <div className="flex items-center">
                        <span className="w-32 text-cyan-700">Áp suất:</span>
                        <span className="font-medium">
                            {data.predicted_pressure.toFixed(1)} hPa
                        </span>
                    </div>
                </div>
                )}
            </div>
        </div>
    );
}

export default PredictionPage;