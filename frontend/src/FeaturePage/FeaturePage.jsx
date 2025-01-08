// src/pages/FeaturePage.js
import React, { useEffect, useState } from 'react';
import { fetchSentiment, postDistribution, recentFinancialData } from './services/api';
import SentimentCard from './SentimentCard/SentimentCard.jsx';
import PopularPosts from './PopularPosts/PopularPosts.jsx';
import FinancialDataChart from './FinancialDataChart/FinancialDataChart.jsx';

const FeaturePage = () => {
  // State management
  const [sentimentData, setSentimentData] = useState(null);
  const [averageSentiment, setAverageSentiment] = useState(null);
  const [financialData, setFinancialData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const post_distribution = await postDistribution();
		const avg_sentiment = await fetchSentiment(); 
        const financial = await recentFinancialData();

        setSentimentData(post_distribution);
		setAverageSentiment(avg_sentiment);
        setFinancialData(financial);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(true);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl font-semibold">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-red-500 text-xl font-semibold">
          Failed to load data. Please try again later.
        </div>
      </div>
    );
  }

  return (
    <main className="container mx-auto p-6">
      {/* Sentiment Analysis Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-4">Sentiment Analysis</h2>
        {sentimentData && <SentimentCard data={sentimentData} average={averageSentiment} />}
      </section>

      {/* Popular Posts Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-4">Recent Posts</h2>
        	<PopularPosts />
      </section>

      {/* Financial Data Section */}
	  <section className="mb-12">
        <h2 className="text-3xl font-bold mb-4">Recent Financial Data</h2>
        {financialData && <FinancialDataChart data={financialData} />}
      </section>
    </main>
  );
};

export default FeaturePage;
