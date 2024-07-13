import React, { useState, useEffect, useRef, useCallback } from "react";
import * as d3 from "d3";

const CryptoPriceGraph = () => {
  const [timeFrame, setTimeFrame] = useState("year");
  const [crypto, setCrypto] = useState("bitcoin");
  const svgRef = useRef();

  const drawChart = useCallback(
    (prices) => {
      d3.select(svgRef.current).selectAll("*").remove();

      const margin = { top: 40, right: 30, bottom: 50, left: 60 };
      const width = 800 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      const svg = d3
        .select(svgRef.current)
        .attr("width", width + margin.left + margin.right + 25)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3
        .scaleTime()
        .domain(d3.extent(prices, (d) => d.date))
        .range([0, width]);

      const yMin = d3.min(prices, (d) => d.value);
      const yMax = d3.max(prices, (d) => d.value);
      const yRange = yMax - yMin;
      const yPadding = yRange * 0.1; // 10% padding above and below

      const y = d3
        .scaleLinear()
        .domain([yMin - yPadding, yMax + yPadding])
        .range([height, 0]);

      const line = d3
        .line()
        .x((d) => x(d.date))
        .y((d) => y(d.value));

      svg
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .attr("color", "#9CA3AF")
        .selectAll("text")
        .style("font-size", "12px");

      svg
        .append("g")
        .call(d3.axisLeft(y).ticks(10))
        .attr("color", "#9CA3AF")
        .selectAll("text")
        .style("font-size", "12px");

      svg
        .append("path")
        .datum(prices)
        .attr("fill", "none")
        .attr("stroke", "#EAB308")
        .attr("stroke-width", 2)
        .attr("d", line);

      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", 0 - margin.top / 2)
        .attr("text-anchor", "middle")
        .style("font-size", "24px")
        .style("fill", "#EAB308")
        .text(
          `${crypto.charAt(0).toUpperCase() + crypto.slice(1)} Price - ${
            timeFrame.charAt(0).toUpperCase() + timeFrame.slice(1) + "ly"
          }`
        );

      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", height + margin.bottom - 10)
        .attr("text-anchor", "middle")
        .style("font-size", "14px")
        .style("fill", "#9CA3AF")
        .text("Date");

      svg
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left - 2)
        .attr("x", -1 - height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .style("font-size", "14px")
        .style("fill", "#9CA3AF")
        .text("Price (USD)");

      // Add hover effects
      const focus = svg
        .append("g")
        .attr("class", "focus")
        .style("display", "none");

      focus.append("circle").attr("r", 5).attr("fill", "#EAB308");

      focus
        .append("rect")
        .attr("class", "tooltip")
        .attr("width", 100)
        .attr("height", 50)
        .attr("x", 10)
        .attr("y", -22)
        .attr("rx", 4)
        .attr("ry", 4)
        .style("fill", "white")
        .style("opacity", 0.7);

      focus
        .append("text")
        .attr("class", "tooltip-date")
        .attr("x", 18)
        .attr("y", -2)
        .style("font-size", "12px");

      focus
        .append("text")
        .attr("class", "tooltip-price")
        .attr("x", 18)
        .attr("y", 18)
        .style("font-size", "12px")
        .style("font-weight", "bold");

      svg
        .append("rect")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .style("opacity", 0)
        .on("mouseover", () => focus.style("display", null))
        .on("mouseout", () => focus.style("display", "none"))
        .on("mousemove", mousemove);

      const bisectDate = d3.bisector((d) => d.date).left;

      function mousemove(event) {
        const x0 = x.invert(d3.pointer(event)[0]);
        const i = bisectDate(prices, x0, 1);
        const d0 = prices[i - 1];
        const d1 = prices[i];
        const d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        focus.attr("transform", `translate(${x(d.date)},${y(d.value)})`);
        focus.select(".tooltip-date").text(d.date.toLocaleDateString());
        focus.select(".tooltip-price").text(`$${d.value.toFixed(2)}`);
      }
    },
    [crypto, timeFrame]
  );

  useEffect(() => {
    const fetchData = async () => {
      const days = timeFrame === "year" ? 365 : timeFrame === "month" ? 30 : 1;
      const response = await fetch(
        `https://api.coingecko.com/api/v3/coins/${crypto}/market_chart?vs_currency=usd&days=${days}&interval=daily`
      );
      const data = await response.json();
      const prices = data.prices.map((price) => ({
        date: new Date(price[0]),
        value: price[1],
      }));

      drawChart(prices);
    };

    fetchData();
  }, [timeFrame, crypto, drawChart]);

  return (
    <div className="crypto-graph bg-black p-4 rounded-lg">
      <div className="mb-4 flex justify-center space-x-4">
        <select
          value={timeFrame}
          onChange={(e) => setTimeFrame(e.target.value)}
          className="bg-gray-800 text-gray-200 rounded p-2"
        >
          <option value="year">1 Year</option>
          <option value="month">1 Month</option>
          <option value="day">1 Day</option>
        </select>
        <select
          value={crypto}
          onChange={(e) => setCrypto(e.target.value)}
          className="bg-gray-800 text-gray-200 rounded p-2"
        >
          <option value="bitcoin">Bitcoin</option>
          <option value="ethereum">Ethereum</option>
          <option value="solana">Solana</option>
        </select>
      </div>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default CryptoPriceGraph;
