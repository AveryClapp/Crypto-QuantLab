import React from "react";
import { useRef, useEffect, useState } from "react";
import Graph from "../../Common/Graph.jsx";

export default function TradeInfo() {
  const fadeRef = useRef(null);
  const [opacity, setOpacity] = useState(0);
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setOpacity(1);
          } else {
            setOpacity(0);
          }
        });
      },
      {
        threshold: 0.1, // Trigger when 10% of the element is visible
      }
    );

    if (fadeRef.current) {
      observer.observe(fadeRef.current);
    }

    // Capture the current value of fadeRef
    const currentRef = fadeRef.current;

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, []);
  return (
    <section className="h-full bg-black" id="services">
      <div className="h-full flex flex-col items-center bg-black rounded text-gray-200">
        <h1 className="mt-32 text-7xl">
          <span className="text-yellow-500">Trade </span>
          Crypto Better
        </h1>
        <h2 className="text-5xl pt-1 pb-5">
          We give you <span className="text-yellow-500">an edge...</span>
        </h2>
        <Graph />
      </div>
      <div
        ref={fadeRef}
        style={{
          opacity: opacity,
          transition: "opacity 0.5s ease-in-out",
        }}
        className="p-5 rounded-lg text-white relative grid grid-cols-4 grid-rows-2"
      >
        <div className="col-start-1 pb-4 row-span-1 flex justify-center items-center">
          <h3 className="font-bold text-5xl text-yellow-500 pb-4 ">Why?</h3>
        </div>
        <p className="text-lg row-span-1 font-bold col-start-2 col-span-2">
          <span className="text-yellow-500 text-xl font-bold">
            The Crypto Market Is Evolving.{" "}
          </span>
          New tools are emerging to boost profitability. As technology
          integrates with finance, leveraging these innovations becomes crucial
          for success in trading.
        </p>
        <div className="col-start-2 row-start-2 flex justify-center items-center">
          <h3 className="font-bold text-5xl text-yellow-500">How?</h3>
        </div>
        <p className="text-lg row-start-2 font-bold col-start-3 col-span-2">
          <span className="text-yellow-500 text-xl font-bold">
            AI-Powered Solutions.{" "}
          </span>
          Harness the power of machines. Our platform integrates Natural
          Language Processing for sentiment analysis and Machine Learning for
          predictive modeling, offering unprecedented advantages in crypto
          trading.
        </p>
      </div>
    </section>
  );
}
