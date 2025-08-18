import axios from 'axios';

const axiosFA = axios.create({
  baseURL: ' https://summaryai-6tu0.onrender.com/',
  headers: {
    'Content-Type': 'application/json',
  },
});
export default axiosFA;
