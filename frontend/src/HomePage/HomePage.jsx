import React from 'react';
import Home from "./Home/Home.jsx";
import Header from "./Header/Header.jsx";
import TradeInfo from "./TradeInfo/TradeInfo.jsx";
import Footer from "./Footer/Footer.jsx";
import Sell from "./Sell/Sell.jsx";

const HomePage = () => {
	return (
		<main>
			<Header />	
			<Home />
			<TradeInfo />
			<Sell />
			<Footer />
		</main>
	)
}

export default HomePage;
