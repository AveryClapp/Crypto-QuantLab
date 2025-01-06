import React, { useState, useEffect } from "react";
import { CCarousel, CCarouselItem, CImage } from "@coreui/react";
import learnCryptoImage from "../../assets/learn_crypto.jpeg";
import tradeCryptoImage from "../../assets/trade_crypto.png";
import analyzeCryptoImage from "../../assets/analyze_crypto.jpeg";
import Header from "../Header/Header.jsx";
import TradeInfo from "../TradeInfo/TradeInfo.jsx";
import Footer from "../Footer/Footer.jsx";
import Sell from "../Sell/Sell.jsx";


const slides = [
  { image: tradeCryptoImage, alt: "Trade Crypto", text: "Trade" },
  { image: learnCryptoImage, alt: "Learn Crypto", text: "Test" },
  { image: analyzeCryptoImage, alt: "Analyze Crypto", text: "Learn" },
];

export default function Home() {
  const [actionText, setActionText] = useState("Trade");
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    setActionText(slides[activeIndex].text);
  }, [activeIndex]);

  const handleSlide = (index) => {
    setActiveIndex(index);
  };

  return (
    <div
      className="relative h-screen w-full overflow-hidden bg-black"
      id="home"
    >
      <div className="absolute -top-48 -left-96 w-1/2 h-3/4 bg-red-500 rounded-full blur-3xl bg-opacity-40"></div>
      <div className="absolute -bottom-48 -left-10 w-1/3 h-1/2 bg-purple-600 rounded-full blur-3xl bg-opacity-30"></div>
      <div className="absolute bottom-48 -right-80 w-1/2 h-1/2 bg-orange-500 rounded-full blur-3xl bg-opacity-40"></div>

      {/* Content */}
      <div className="relative z-10 flex items-center justify-center h-full flex-col pt-10">
        <h1 className="text-yellow-500 font-bold text-5xl transition-all duration-500 ease-in-out">
          {actionText}
        </h1>
        <h2 className="text-6xl font-bold text-white text-center mb-7">
          Cryptocurrencies
        </h2>
        <CCarousel
          controls
          indicators
          transition="crossfade"
          onSlide={handleSlide}
          className="w-full max-w-2xl"
          dark
        >
          {slides.map((slide, index) => (
            <CCarouselItem key={index}>
              <CImage
                className="w-full h-48 sm:h-64 md:h-80 lg:h-96 object-cover object-center"
                src={slide.image}
                alt={slide.alt}
              />
            </CCarouselItem>
          ))}
        </CCarousel>
      </div>
    </div>
  );
}
