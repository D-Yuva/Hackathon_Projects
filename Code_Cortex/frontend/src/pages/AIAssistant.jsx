import React, { useState } from "react";
import axios from "axios";

const Assistant = () => {
  const [data1File, setData1File] = useState(null);
  const [data2File, setData2File] = useState(null);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const handleUpload = async () => {
    if (!data1File || !data2File) {
      alert("Please upload both CSV files.");
      return;
    }

    const formData = new FormData();
    formData.append("data1", data1File);
    formData.append("data2", data2File);

    try {
      const result = await axios.post("http://localhost:5000/upload_csv", formData);
      alert(result.data.message);
    } catch (error) {
      alert("Error uploading CSV files.");
    }
  };

  const handleQuery = async () => {
    try {
      const result = await axios.post("http://localhost:5000/query", { query });
      setResponse(result.data);
    } catch (error) {
      alert("Error processing query.");
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">AI Chat Assistant for Efficiency Analysis</h1>

      <div className="mb-4">
        <label className="block text-sm font-medium">Upload CSV Data1</label>
        <input type="file" onChange={(e) => setData1File(e.target.files[0])} />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium">Upload CSV Data2</label>
        <input type="file" onChange={(e) => setData2File(e.target.files[0])} />
      </div>

      <button
        className="bg-blue-500 text-white py-2 px-4 rounded mb-4"
        onClick={handleUpload}
      >
        Upload CSVs
      </button>

      <div className="mb-4">
        <label className="block text-sm font-medium">Enter Your Query</label>
        <textarea
          className="border p-2 w-full"
          rows="3"
          onChange={(e) => setQuery(e.target.value)}
          value={query}
        ></textarea>
      </div>

      <button
        className="bg-green-500 text-white py-2 px-4 rounded"
        onClick={handleQuery}
      >
        Submit Query
      </button>

      {response && (
        <div className="mt-6">
          <h3 className="text-xl font-bold">Generated Answer</h3>
          <p className="bg-gray-100 p-4 rounded">{response.generated_answer}</p>

          <h3 className="text-xl font-bold mt-4">AI Recommendations</h3>
          <p className="bg-gray-100 p-4 rounded">{response.recommendation}</p>
        </div>
      )}
    </div>
  );
};

export default Assistant;
