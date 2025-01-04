import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Label,
} from "recharts";

const InteractiveGraph = () => {
  const location = useLocation();
  const { originalData, predictedData } = location.state || {};
  const [chartData, setChartData] = useState([]);
  const [selectedField, setSelectedField] = useState("RT");
  const [inputValue, setInputValue] = useState("");
  const [predictedEfficiency, setPredictedEfficiency] = useState(null);
  
  const fields = [
    "RT",
    "KW_TOT",
    "CH LOAD",
    "DeltaCT",
    "Hz_CHP",
    "CDHI",
    "Hz_CDS",
    "Hz_CT",
    "Precent_CT",
    "RH%",
  ];

  useEffect(() => {
    if (originalData && predictedData) {
      const formattedData = originalData.map((row, index) => ({
        ...row,
        Predicted_Efficiency: predictedData.Predicted_Efficiency[index],
      }));

      setChartData(formattedData);
    }
  }, [originalData, predictedData]);

  const handleFieldChange = (e) => {
    setSelectedField(e.target.value);
    setInputValue("");
    setPredictedEfficiency(null);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    const fieldData = chartData.map(data => data[selectedField]);
    const efficiencyData = chartData.map(data => data.Predicted_Efficiency);
    if (fieldData.length > 0) {
      const predictedEff = predictEfficiency(fieldData, efficiencyData, value);
      setPredictedEfficiency(predictedEff);
    }
  };

  const predictEfficiency = (fieldData, efficiencyData, input) => {
    const inputValue = parseFloat(input);
    const index = fieldData.findIndex(value => value >= inputValue);
    if (index === -1) return NaN;
    if (index === 0) return efficiencyData[0];
    if (index === fieldData.length - 1) return efficiencyData[efficiencyData.length - 1];

    const x0 = fieldData[index - 1];
    const x1 = fieldData[index];
    const y0 = efficiencyData[index - 1];
    const y1 = efficiencyData[index];

    return y0 + ((inputValue - x0) / (x1 - x0)) * (y1 - y0);
  };

  const sortedChartData = [...chartData].sort((a, b) => a[selectedField] - b[selectedField]);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Interactive Efficiency Graph</h1>
      <p className="text-gray-600 mb-6">
        Select a field to plot against predicted efficiency.
      </p>

      <div className="flex mb-4">
        <select onChange={handleFieldChange} value={selectedField} className="mr-4 bg-blue-400">
          {fields.map((field) => (
            <option key={field} value={field}>
              {field}
            </option>
          ))}
        </select>

        <input
          type="number"
          value={inputValue}
          onChange={handleInputChange}
          placeholder={`Enter ${selectedField} value`}
          className="border rounded p-2 w-32 bg-blue-700"
        />
      </div>

      {predictedEfficiency !== null && (
        <p className="text-blue-600 mb-4">
          Predicted Efficiency: {isNaN(predictedEfficiency) ? "Out of range" : predictedEfficiency.toFixed(2)}
        </p>
      )}

      {sortedChartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={sortedChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey={selectedField}
              label={{ value: selectedField, position: 'insideBottom' }} 
              domain={[0, 'dataMax']}
            />
            <YAxis 
              dataKey="Predicted_Efficiency"
              tickFormatter={(value) => {
                const numericValue = Number(value);
                return !isNaN(numericValue) ? numericValue.toFixed(1) : value;
              }}
            >
              <Label value="Predicted Efficiency" angle="-90" position="insideLeft" />
            </YAxis>
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Line type="monotone" dataKey="Predicted_Efficiency" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-gray-600">Loading chart data...</p>
      )}
    </div>
  );
};

export default InteractiveGraph;
