import React, {useEffect, useState} from "react";
import {getLocation, insertLocation} from "../services/Api.js";
import {toast} from "react-toastify";
import {Box, Button, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography,} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import VisibilityIcon from "@mui/icons-material/Visibility";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import MapModal from "../components/modals/MapModal.jsx";
import MapViewModal from "../components/modals/MapViewModal.jsx";

function Locations() {
    const [locations, setLocations] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [mapOpened, setMapOpened] = useState(false);
    const [mapViewOpened, setMapViewOpened] = useState(false);
    const [viewLocation, setViewLocation] = useState(null);

    const [newLocation, setNewLocation] = useState({
        name: "",
        latitude: "",
        longitude: "",
        address: "",
    });

    useEffect(() => {
        getLocation({})
            .then((response) => {
                setLocations(response.data);
            })
            .catch((error) => {
                toast.error(error.response);
            });
    }, []);


    useEffect(() => {
        if (viewLocation) {
            setMapViewOpened(true)
        }
    }, [viewLocation]);
    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setNewLocation({...newLocation, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            setModalOpened(false);

            insertLocation(newLocation)
                .then((response) => {
                    setLocations([...locations, response.data]);
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

            <Box display="flex" justifyContent="flex-end" my={2}>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddCircleIcon/>}
                    onClick={() => setModalOpened(true)}
                >
                    Add NEW
                </Button>
            </Box>

            {/* Add Location Modal */}
            <ModalLayout title={"New Location"} modalOpened={modalOpened} setModalOpened={setModalOpened}>
                <Box component="form" onSubmit={handleSubmit} sx={{p: 2}}>
                    <Typography variant="h6" sx={{mb: 2}}>
                        Add New Location
                    </Typography>

                    {/* Name Input */}
                    <TextField
                        label="Name"
                        name="name"
                        value={newLocation.name}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                        required
                    />

                    {/* Select Location Button - Centered */}
                    <Box sx={{display: "flex", justifyContent: "center", mt: 2}}>
                        <Button variant="outlined" onClick={() => setMapOpened(true)}>
                            Select Location on Map
                        </Button>
                    </Box>

                    {/* Show selected location details */}
                    {newLocation.latitude && (
                        <Box sx={{textAlign: "center", mt: 2, p: 2, bgcolor: "#f9f9f9", borderRadius: "8px"}}>
                            <Typography variant="body1">
                                <strong>Latitude:</strong> {newLocation.latitude}, <strong>Longitude:</strong> {newLocation.longitude}
                            </Typography>
                            <Typography variant="body2">
                                <strong>Address:</strong> {newLocation.address}
                            </Typography>
                        </Box>
                    )}

                    {/* Save Button - Centered */}
                    <Box sx={{display: "flex", justifyContent: "center", mt: 3}}>
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            sx={{width: "40%"}}
                            disabled={!newLocation.latitude || !newLocation.longitude} // Disable until location is selected
                        >
                            Save
                        </Button>

                    </Box>
                </Box>
            </ModalLayout>


            {/* Map Modal */}
            <ModalLayout title={"Select Location"} modalOpened={mapOpened} setModalOpened={setMapOpened}>
                <MapModal setNewLocation={setNewLocation} setModalOpened={setMapOpened}/>
            </ModalLayout>


            {/* View Location Modal */}
            {viewLocation && (
                <ModalLayout title={"View Location"} modalOpened={mapViewOpened} setModalOpened={setMapViewOpened}>
                    <MapViewModal
                        setNewLocation={setNewLocation}
                        setModalOpened={setMapViewOpened}
                        viewLocation={viewLocation}
                    />
                </ModalLayout>
            )}

            {/* Locations Table */}
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
                        {locations.map((loc) => (
                            <TableRow key={loc.id}>
                                <TableCell>{loc.id}</TableCell>
                                <TableCell>{loc.name}</TableCell>
                                <TableCell>{loc.latitude}</TableCell>
                                <TableCell>{loc.longitude}</TableCell>
                                <TableCell>{loc.address}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        color="secondary"
                                        startIcon={<VisibilityIcon/>}
                                        onClick={() => {
                                            setViewLocation({lat: loc.latitude, lng: loc.longitude})
                                        }}
                                    >
                                        View
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

export default Locations;
