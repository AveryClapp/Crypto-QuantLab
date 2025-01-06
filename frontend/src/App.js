import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage/HomePage.jsx";
import FeaturePage from "./FeaturePage/FeaturePage.jsx";

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/features" element={<FeaturePage />} />
        </Routes>
    </Router>
  );
}

export default App;
