import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Vehicles() {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    // Fetch vehicles from Django backend
    axios.get('/api/vehicles/')
      .then(response => setVehicles(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center">Vehicles</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Vehicle ID</th>
            <th>Make</th>
            <th>Model</th>
            <th>Year</th>
            <th>VIN</th>
            <th>Mileage</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map(vehicle => (
            <tr key={vehicle.id}>
              <td>{vehicle.id}</td>
              <td>{vehicle.make}</td>
              <td>{vehicle.model}</td>
              <td>{vehicle.year}</td>
              <td>{vehicle.vin}</td>
              <td>{vehicle.current_mileage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Vehicles;