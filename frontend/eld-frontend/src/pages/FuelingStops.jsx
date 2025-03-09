import React, { useEffect, useState } from 'react';
import axios from 'axios';

function FuelingStops() {
  const [fuelingStops, setFuelingStops] = useState([]);

  useEffect(() => {
    // Fetch fueling stops from Django backend
    axios.get('/api/fueling-stops/')
      .then(response => setFuelingStops(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center">Fueling Stops</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Fueling ID</th>
            <th>Trip</th>
            <th>Location</th>
            <th>Fuel Amount</th>
            <th>Fuel Cost</th>
            <th>Mileage</th>
          </tr>
        </thead>
        <tbody>
          {fuelingStops.map(fueling => (
            <tr key={fueling.id}>
              <td>{fueling.id}</td>
              <td>{fueling.trip}</td>
              <td>{fueling.location}</td>
              <td>{fueling.fuel_amount}</td>
              <td>{fueling.fuel_cost}</td>
              <td>{fueling.mileage_at_fueling}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FuelingStops;