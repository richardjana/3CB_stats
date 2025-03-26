import { useState, useEffect } from 'react';
import axios from 'axios';

const use3cbApi = (endpoint) => {
  const baseUrl = 'http://127.0.0.1:5000/'; // Define the base URL here
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`${baseUrl}${endpoint}`);
        setData(response.data);
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        setErrorMessage(error.response?.data || 'An error occurred.');
      }
    };

    fetchData(); // Fetch data once when the component mounts or when `endpoint` changes

  }, [endpoint]); // Dependency array with `endpoint` ensures it fetches only when the endpoint changes

  return { data, isLoading, errorMessage };
};

export default use3cbApi;
