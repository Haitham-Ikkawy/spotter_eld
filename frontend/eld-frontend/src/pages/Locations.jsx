import React, {useEffect, useState} from 'react';
import {GetTrips, insertLocation, insertTrips} from "../services/Api.js";
import {toast} from "react-toastify";
import {Box, Button, Container, Modal, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";

function Locations() {
    const [locations, setLocations] = useState([]);
    const [open, setOpen] = useState(false);
    const [newLocation, setNewLocation] = useState({
        name: '',
        latitude: '',
        longitude: '',  // ✅ Use correct state keys
        address: '',
    });

    // Fetch locations from the backend
    useEffect(() => {
        GetTrips({})
            .then((response) => {
                setLocations(response.data);
            })
            .catch((error) => {
                toast.error(error.response);
            });
    }, []);

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setNewLocation({...newLocation, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            setOpen(false);

            insertLocation(newLocation)
                .then((response) => {
                    console.log("response", response.data);
                    setLocations([...locations, response.data]); // ✅ Update UI with new trip
                })
                .catch((error) => {
                    toast.error(error.response);
                });
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Container>
            <PageTitle title="Locations"/>

            {/* Add Trip Modal */}
            <Modal open={open} onClose={() => setOpen(false)}>
                <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '80%',
                    maxWidth: 400,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    p: 4,
                    borderRadius: 2
                }}>
                    <Typography variant="h6" gutterBottom>
                        Add New Trip
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit}>
                        <TextField label="Name" name="name" value={newLocation.driver} onChange={handleInputChange} fullWidth margin="normal" required/>
                        <TextField label="Latitude" name="latitude" value={newLocation.vehicle} onChange={handleInputChange} fullWidth margin="normal" required/>
                        <TextField label="Longitude" name="longitude" value={newLocation.start_location} onChange={handleInputChange} fullWidth margin="normal" required/>
                        <TextField label="Address" name="address" value={newLocation.end_location} onChange={handleInputChange} fullWidth margin="normal" required/>
                        <Button type="submit" variant="contained" color="primary" sx={{mt: 2}}>Save Trip</Button>
                    </Box>
                </Box>
            </Modal>

            {/* Trips Table */}
            <TableContainer component={Paper} sx={{mt: 4}}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Latitude</TableCell>
                            <TableCell>Longitude</TableCell>
                            <TableCell>Address</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {locations.map(trip => (
                            <TableRow key={trip.id}>
                                <TableCell>{trip.id}</TableCell>
                                <TableCell>{trip.name}</TableCell>
                                <TableCell>{trip.latitude}</TableCell>
                                <TableCell>{trip.longitude}</TableCell> {/* ✅ Use correct key */}
                                <TableCell>{trip.address}</TableCell> {/* ✅ Use correct key */}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

export default Locations;