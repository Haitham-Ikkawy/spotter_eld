import React, { useState, useEffect } from 'react';
import { GoogleMap, Marker, DirectionsRenderer } from '@react-google-maps/api';

const Map = ({ pickupLocation, dropoffLocation }) => {
  const [directions, setDirections] = useState(null);

  useEffect(() => {
    const directionsService = new window.google.maps.DirectionsService();
    directionsService.route(
      {
        origin: pickupLocation,
        destination: dropoffLocation,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          setDirections(result);
        }
      }
    );
  }, [pickupLocation, dropoffLocation]);

  return (
    <GoogleMap
      zoom={10}
      center={pickupLocation}
      mapContainerStyle={{ width: '100%', height: '400px' }}
    >
      {directions && <DirectionsRenderer directions={directions} />}
    </GoogleMap>
  );
};

export default Map;