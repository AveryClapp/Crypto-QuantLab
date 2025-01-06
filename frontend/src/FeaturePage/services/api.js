import axios from 'axios';

const API_URL = 'http://0.0.0.0:8000/api'

// Sentiment APIs
export const fetchSentiment = async (timespan) => {
    console.log(timespan);
    try {
        const response = await axios.get(`${API_URL}/sentiment/${timespan}`);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}
export const popularPosts = async (number) => {
    try {
        const response = await axios.get(`${API_URL}/hot_article/${number}`);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}


// Financial APIs
export const recentFinancialData = async (number) => {
    try {
        const response = await axios.get(`${API_URL}/financial_data/${number}`);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}

