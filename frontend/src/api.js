// api.js
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Update with your backend URL

const createItem = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/add_item`, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export { createItem };
