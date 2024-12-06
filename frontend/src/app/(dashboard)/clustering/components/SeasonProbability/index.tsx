import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const defaultStartDate = '2023-11-20';
const defaultEndDate = '2024-12-06';

const defaultProbabilities = {
    spring: 0,
    summer: 0,
    autumn: 0,
    winter: 0
};

function SeasonProbability() {
    const [selectedDate, setSelectedDate] = useState(defaultEndDate);
    const [probabilities, setProbabilities] = useState(defaultProbabilities);

    const { data, refetch } = useQuery({
        queryKey: ['season-probability', selectedDate],
        queryFn: async () => {
            const response = await axios.get(
                `http://localhost:8000/api/clustering/season-probability?date=${selectedDate}`
            );
            return response.data;
        },
        enabled: false
    });

    useEffect(() => {
        if (data) {
            setProbabilities(data);
        }
    }, [data]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        refetch();
    };

    return (
        <div className="h-full flex flex-col">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4 mb-6">
                <div>
                    <label htmlFor="date" className="text-sm font-medium text-cyan-700">
                        Chọn ngày
                    </label>
                    <input
                        type="date"
                        id="date"
                        value={selectedDate}
                        min={defaultStartDate}
                        max={defaultEndDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                        className="mt-1 block w-full border border-slate-200 rounded-md p-2
                                 focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                    />
                </div>
                <button
                    type="submit"
                    className="bg-sky-500 text-white py-2 px-4 rounded-md hover:bg-sky-600
                             transition-colors duration-200"
                >
                    Xác nhận
                </button>
            </form>

            <div className="flex-1 flex flex-col justify-center">
                <h3 className="text-base font-medium text-cyan-700 mb-3">
                    Kết quả dự đoán
                </h3>
                <div className="space-y-3">
                    {[
                        { season: 'Xuân', value: probabilities.spring },
                        { season: 'Hạ', value: probabilities.summer },
                        { season: 'Thu', value: probabilities.autumn },
                        { season: 'Đông', value: probabilities.winter },
                    ].map(({ season, value }) => (
                        <div key={season} className="flex items-center">
                            <span className="w-16 text-cyan-700">{season}:</span>
                            <div className="flex-1 h-4 bg-slate-100 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-sky-500 transition-all duration-500"
                                    style={{ width: `${value}%` }}
                                />
                            </div>
                            <span className="ml-3 w-16 text-right text-cyan-700">
                                {value.toFixed(1)}%
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default SeasonProbability;