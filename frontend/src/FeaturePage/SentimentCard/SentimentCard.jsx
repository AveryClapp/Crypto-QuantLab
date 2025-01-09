// src/components/SentimentCard.js
import React, { useEffect, useState } from 'react';

const SentimentCard = ({ data, average }) => {
	const [positivePercentage, setPositivePercentage] = useState("");
	const [neutralPercentage, setNeutralPercentage] = useState("");
	const [negativePercentage, setNegativePercentage] = useState("");
	
	useEffect(() => {
		function calculatePercentages() {
				if (data) {
						const numPositive = data[0].length;
						const numNeutral = data[2].length;
						const numNegative = data[1].length;
						const totalPosts = numPositive + numNeutral + numNegative;
						setPositivePercentage(`${Math.round((numPositive / totalPosts) * 100)}%`);
						setNeutralPercentage(`${Math.round((numNeutral / totalPosts) * 100)}%`);
						setNegativePercentage(`${Math.round((numNegative / totalPosts) * 100)}%`);
				} else {
						setPositivePercentage("0%");
						setNeutralPercentage("0%");
						setNegativePercentage("0%");
				}
		};
		calculatePercentages();
	}
	, [data]);

  return (
    <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-semibold mb-2">{data.title}</h3>
      <p className="mb-4">{data.description}</p>
      {/* Example Sentiment Metrics */}
      <div className="flex space-x-4">
        <div>
          <span className="font-bold">Positive:</span> {positivePercentage}
        </div>
        <div>
          <span className="font-bold">Neutral:</span> {neutralPercentage}
        </div>
        <div>
          <span className="font-bold">Negative:</span> {negativePercentage}
        </div>
		<div>
		  <span className="font-bold">Average Sentiment Score:</span> {Math.round(average * 100) + "%"}
		</div>
      </div>
    </div>
  );
};

export default SentimentCard;
