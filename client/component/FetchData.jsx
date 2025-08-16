import React, { useEffect, useState } from 'react';

const cardStyle = {
  border: '1px solid #ccc',
  borderRadius: '10px',
  padding: '20px',
  width: '300px',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  backgroundColor: '#f9f9f9',
  fontFamily: 'Arial, sans-serif',
};

const imageStyle = {
  width: '100%',
  borderRadius: '8px',
  marginBottom: '15px',
};

const titleStyle = {
  fontSize: '18px',
  fontWeight: 'bold',
  marginBottom: '10px',
};

const textStyle = {
  marginBottom: '8px',
};

const containerStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '20px',
  maxWidth: '1500px',      
  height: '600px',         
  overflowY: 'auto',      
  margin: '0 auto',
  padding: '20px',
  justifyContent: 'center',
};

const FetchData = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:3000/api/alert-data')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        return response.json();
      })
      .then((jsonData) => {
        setData(jsonData);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }, [setData]);

  return (
    <div>
      <h2 style={{ textAlign: 'center' }}>Fetched Alert Data</h2>
      {data && data.length > 0 ? (
        <div style={containerStyle}>
          {data.map((item) => (
            <div key={item._id} style={cardStyle}>
              <img src={item.image_url} alt="Fetched Visual" style={imageStyle} />
              <div style={titleStyle}>Location Details</div>
              <div style={textStyle}><strong>Latitude:</strong> {item.latitude}</div>
              <div style={textStyle}><strong>Longitude:</strong> {item.longitude}</div>
              <div style={textStyle}><strong>Address:</strong> {item.address}</div>
              <div style={textStyle}><strong>Timestamp:</strong> {new Date(item.timestamp).toLocaleString()}</div>
            </div>
          ))}
        </div>
      ) : (
        <p style={{ textAlign: 'center' }}>
          {data.length === 0 ? 'No data available.' : 'Loading...'}
        </p>
      )}
    </div>
  );
};

export default FetchData;
