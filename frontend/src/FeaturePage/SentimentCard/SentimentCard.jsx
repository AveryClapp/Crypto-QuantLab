// src/components/SentimentCard.js
import React from 'react';

const SentimentCard = ({ data }) => {
  return (
    <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-semibold mb-2">{data.title}</h3>
      <p className="mb-4">{data.description}</p>
      {/* Example Sentiment Metrics */}
      <div className="flex space-x-4">
        <div>
          <span className="font-bold">Positive:</span> {data.positive}%
        </div>
        <div>
          <span className="font-bold">Neutral:</span> {data.neutral}%
        </div>
        <div>
          <span className="font-bold">Negative:</span> {data.negative}%
        </div>
      </div>
    </div>
  );
};

export default SentimentCard;
