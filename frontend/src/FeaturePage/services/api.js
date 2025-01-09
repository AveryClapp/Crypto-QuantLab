import axios from 'axios';

const API_URL = 'http://0.0.0.0:8000/api'

// Sentiment APIs
export const fetchSentiment = async (timespan=24) => {
    try {
        const response = await axios.get(`${API_URL}/sentiment/${timespan}`);
        return response.data;
 } catch (error) {
        console.log(error);
    }
}
export const popularPosts = async (number=3) => {
    try {
        const response = await axios.get(`${API_URL}/hot_article/${number}`);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}

export const postDistribution = async () => {
    try {
        const positive_articles = await axios.get(`${API_URL}/positive_articles`);
        const negative_articles = await axios.get(`${API_URL}/negative_articles`);
        const neutral_articles  = await axios.get(`${API_URL}/neutral_articles`);
        return [positive_articles.data, negative_articles.data, neutral_articles.data];
    } catch (error) {
        console.log(error);
    }
}

// Financial APIs
export const recentFinancialData = async (number=24) => {
    try {
        const response = await axios.get(`${API_URL}/financial_data/${number}`);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}

