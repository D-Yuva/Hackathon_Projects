import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const Results = () => {
  const location = useLocation();
  const { data } = location.state || {};
  const [chartData, setChartData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (data) {
      const groupedData = data.Predicted_Efficiency.reduce((acc, efficiency, index) => {
        const timeCategory = data.Time_Category[index];
        if (!acc[timeCategory]) {
          acc[timeCategory] = [];
        }
        acc[timeCategory].push(efficiency);
        return acc;
      }, {});

      const formattedData = Object.keys(groupedData).map((key) => {
        const efficiencies = groupedData[key];
        const mean = efficiencies.reduce((sum, val) => sum + val, 0) / efficiencies.length;

        return {
          Time_Category: `Category ${key}`,
          mean,
        };
      });

      setChartData(formattedData);
    }
  }, [data]);

  const goToInteractiveGraph = () => {
    navigate("/graph");
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Efficiency Prediction Results</h1>
      <p className="text-gray-600 mb-6">
        The following graph shows the predicted efficiency of the chiller plant categorized by time.
      </p>

      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Time_Category" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="mean" stroke="#82ca9d" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-gray-600">Loading chart data...</p>
      )}
      <button
        onClick={goToInteractiveGraph}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Go to Interactive Graph
      </button>
    </div>
  );
};

export default Results;
