import React, { useState, useEffect } from "react";
import "./App.css";
// import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from "./Home/Home.jsx";
import Header from "./Header/Header.jsx";
import TradeInfo from "./TradeInfo/TradeInfo.jsx";
import Footer from "./Footer/Footer.jsx";
import Sell from "./Sell/Sell.jsx";

function App() {
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const position = window.pageYOffset;
      setScrollPosition(position);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const calculateBlur = () => {
    const maxBlur = 10; // maximum blur in pixels
    const scrollThreshold = 300; // scroll position at which max blur is achieved
    const blur = Math.min(
      (scrollPosition / scrollThreshold) * maxBlur,
      maxBlur
    );
    return `blur(${blur}px)`;
  };

  return (
    <main>
      <Header />
      <div
        style={{
          filter: calculateBlur(),
          transition: "filter 0.3s ease-out",
        }}
      >
        <Home />
      </div>
      <TradeInfo />
      <Sell />
      <Footer />
    </main>
  );
}

export default App;
