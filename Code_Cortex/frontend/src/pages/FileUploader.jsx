import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; 

const FileUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const csvToJson = (csv) => {
    const lines = csv.split("\n").map(line => line.trim()).filter(line => line);
    const headers = lines[0].split(",").map(header => header.trim());
    const jsonData = lines.slice(1).map(line => {
      const values = line.split(",").map(value => value.trim());
      const jsonObject = {};
  
      headers.forEach((header, index) => {
        jsonObject[header] = values[index];
      });
  
      return jsonObject;
    });
  
    return jsonData;
  };  

  const readCSV = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        const data = csvToJson(text);
        resolve(data);
      };
      reader.onerror = (err) => reject(err);
      reader.readAsText(file);
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMessage("Please upload a file!");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", selectedFile);
    console.log(selectedFile);
  
    try {
      setLoading(true);
      setMessage("");
  
      const response = await axios.post("http://localhost:5000/api/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      if (response.status === 200) {
        const originalData = await readCSV(selectedFile);
        navigate("/graph", { state: { originalData, predictedData: response.data } });
      } else {
        setMessage("Something went wrong!");
      }
    } catch (error) {
    console.error("Error fetching predicted efficiency:", error.response.data);
      setMessage("Error occurred during file upload!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Upload CSV File</h1>
      <p className="text-gray-600 mb-6">
        Upload a CSV file containing the data, and we will analyze it in the Interactive Graph.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Upload File:
          </label>
          <input
            type="file"
            accept=".csv"
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

export default FileUploader;
