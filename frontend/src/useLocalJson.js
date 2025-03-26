import { useState, useEffect } from 'react';

const useLocalJson = (endpoint) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(endpoint);
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        const jsonData = await response.json();
        setData(jsonData);
        setIsLoading(false);
      } catch (error) {
        setIsLoading(false);
        setErrorMessage(error.message || 'An error occurred.');
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, isLoading, errorMessage };
};

export default useLocalJson;
