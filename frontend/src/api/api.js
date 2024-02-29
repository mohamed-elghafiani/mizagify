// api.js

import axios from 'axios';

export const baseURL = 'http://127.0.0.1:5000/api';

export const fetchRestaurantBySlug = async (slug) => {
  const res = await axios.get(`${baseURL}/restaurants/${slug}`);
  if(res.status !== 200) {
    throw Error("Error while fetching restaurant by slug!");
  }
  return res.data;
};

// Fetch restaurants reviews
export const fetchReviewsBySlug = async (slug) => {
    try {
      const res = await axios.get(`${baseURL}/reviews/restaurant/${slug}`);
      return res.data;
    } catch (error) {
      throw Error("Error while fetching reviews!");
    }
};
