import React, {useEffect, useState} from "react";
import {MapContainer, Marker, TileLayer, useMap, useMapEvents} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import {Box, Button, Typography} from "@mui/material";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

const customMarker = new L.Icon({
    iconUrl: markerIconPng,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

const DEFAULT_LOCATION = {lat: 33.8938, lng: 35.5018}; // Beirut as fallback

const MapModal = ({setNewLocation, setModalOpened}) => {
    const [position, setPosition] = useState(DEFAULT_LOCATION);
    const [zoom, setZoom] = useState(15); // Start with moderate zoom
    const [address, setAddress] = useState("Fetching location...");

    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
            ({coords}) => {
                const newLocation = {lat: coords.latitude, lng: coords.longitude};
                setPosition(newLocation);
                fetchAddress(newLocation.lat, newLocation.lng);
                // setZoom(17); // Zoom in on detected location
            },
            (error) => {
                console.error("Geolocation error:", error);
                setAddress("Unable to fetch location. Using default.");
            },
            {enableHighAccuracy: true}
        );
    }, []);

    const fetchAddress = async (lat, lon) => {
        try {
            const res = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
            );
            const data = await res.json();
            setAddress(data.display_name || "Unknown Location");
        } catch (error) {
            console.error("Error fetching address:", error);
            setAddress("Address not found");
        }
    };

    function LocationMarker() {
        useMapEvents({
            click(e) {
                setPosition(e.latlng);
                fetchAddress(e.latlng.lat, e.latlng.lng);
            },
        });

        return <Marker position={position} icon={customMarker} draggable/>;
    }

    function AutoCenter() {
        const map = useMap();
        useEffect(() => {
            map.setView(position, zoom);
        }, [position, zoom, map]);

        return null;
    }

    const handleSave = () => {
        setNewLocation((prev) => ({
            ...prev,
            latitude: position.lat,
            longitude: position.lng,
            address,
        }));
        setModalOpened(false);
    };

    return (
        <Box sx={{width: "100%", height: "450px", position: "relative", background: "#fff", borderRadius: "10px", p: 2}}>
            <MapContainer
                style={{height: "350px", width: "100%", borderRadius: "8px"}}
                zoom={zoom}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                <AutoCenter/>
                <LocationMarker/>
            </MapContainer>

            {/* Fixed Address Box with Background */}
            <Box sx={{p: 2, bgcolor: "#f9f9f9", borderRadius: "8px", textAlign: "center"}}>
                <Typography variant="body1">
                    <strong>Selected Address:</strong> {address}
                </Typography>
            </Box>

            {/* Save Button - Centered */}
            <Box sx={{display: "flex", justifyContent: "center", mt: 2}}>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSave}
                    sx={{width: "50%"}}
                >
                    Save Location
                </Button>
            </Box>
        </Box>
    );
};

export default MapModal;
