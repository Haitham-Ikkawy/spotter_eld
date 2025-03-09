import React, { useEffect, useState } from 'react';
import axios from 'axios';

function RestBreaks() {
  const [restBreaks, setRestBreaks] = useState([]);

  useEffect(() => {
    // Fetch rest breaks from Django backend
    axios.get('/api/rest-breaks/')
      .then(response => setRestBreaks(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center">Rest Breaks</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Break ID</th>
            <th>Driver Log</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {restBreaks.map(breakItem => (
            <tr key={breakItem.id}>
              <td>{breakItem.id}</td>
              <td>{breakItem.driver_log}</td>
              <td>{breakItem.start_time}</td>
              <td>{breakItem.end_time}</td>
              <td>{breakItem.duration}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RestBreaks;