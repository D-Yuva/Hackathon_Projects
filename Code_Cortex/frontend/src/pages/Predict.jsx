import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; 

const Predict = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMessage("Please upload a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      setMessage("");

      const response = await axios.post("http://localhost:5000/api/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 200) {
        navigate("/result", { state: { data: response.data } });
      } else {
        setMessage("Something went wrong!");
      }
    } catch (error) {
      setMessage("Error occurred during file upload!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Predict Efficiency</h1>
      <p className="text-gray-600 mb-6">
        Upload a CSV or Excel file containing the plant details, and we will predict the chiller plant efficiency.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Upload File:
          </label>
          <input
            type="file"
            accept=".csv, .xlsx"
            onChange={handleFileChange}
            className="border rounded p-2 w-full"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300"
          disabled={loading}
        >
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>

      {message && <p className="mt-4 text-blue-600">{message}</p>}
    </div>
  );
};

export default Predict;
