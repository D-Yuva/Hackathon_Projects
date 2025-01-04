import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./pages/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Predict from "./pages/Predict.jsx";
import Results from "./pages/Result.jsx";
import InteractiveGraph from "./pages/InteractiveGraph.jsx";
import FileUploader from "./pages/FileUploader.jsx";
import Assistant from "./pages/AIAssistant.jsx";

function App() {
  return (
    <Router>
      <div className="bg-gray-200 text-white min-h-screen">
        <Navbar />
        <div className="container mx-auto py-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/result" element={<Results />} />
            <Route path="/graph" element={<InteractiveGraph />} />
            <Route path="/upload" element={<FileUploader />} />
            <Route path="/assistant" element={<Assistant />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
