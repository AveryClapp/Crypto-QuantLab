import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from "./Home/Home.jsx";
import Header from "./Header/Header.jsx";

function App() {
  return (
    <main>
      <Header />
      <Home />
    </main>
  );
}

export default App;
