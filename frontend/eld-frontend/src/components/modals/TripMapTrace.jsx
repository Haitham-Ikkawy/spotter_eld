import React from "react";
import {MapContainer, Marker, Polyline, Popup, TileLayer} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import {Box, Typography} from "@mui/material";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

const customMarker = new L.Icon({
    iconUrl: markerIconPng,
    iconSize: [30, 45],
    iconAnchor: [15, 45],
});

const TripMapTrace = ({tripTrace}) => {

    console.log("tripTrace", tripTrace)
    if (!tripTrace || !tripTrace.actions || tripTrace.actions.length === 0) {
        return <Typography variant="h6">No trip trace data available.</Typography>;
    }

    const positions = tripTrace.actions.map(action => [action.location.latitude, action.location.longitude]);

    return (
        <Box sx={{width: "100%", height: "500px", position: "relative", background: "#fff", borderRadius: "10px", p: 2}}>
            <MapContainer
                style={{height: "450px", width: "100%", borderRadius: "8px"}}
                center={positions[0]}
                zoom={12}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

                {/* Route Trace */}
                <Polyline positions={positions} color="blue" weight={4} opacity={0.7}/>

                {/* Markers with Popups */}
                {tripTrace.actions.map((action, index) => (
                    <Marker key={index} position={[action.location.latitude, action.location.longitude]} icon={customMarker}>
                        <Popup>
                            <Typography variant="body1"><strong>{action.type}</strong></Typography>
                            <Typography variant="body2">Date: {new Date(action._dt).toLocaleString()}</Typography>
                            {action.duration && <Typography variant="body2">Duration: {action.duration} minutes</Typography>}
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </Box>
    );
};

export default TripMapTrace;
