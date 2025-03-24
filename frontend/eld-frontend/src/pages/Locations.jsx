import React, {useEffect, useState} from "react";
import {getLocation, insertLocation} from "../services/Api.js";
import {toast} from "react-toastify";
import {
    Box,
    Button,
    CircularProgress,
    Container,
    FormControl,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import VisibilityIcon from "@mui/icons-material/Visibility";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import MapModal from "../components/modals/MapModal.jsx";
import MapViewModal from "../components/modals/MapViewModal.jsx";
import Constants from "../common/constants.js";

function Locations() {
    const [locations, setLocations] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [mapOpened, setMapOpened] = useState(false);
    const [mapViewOpened, setMapViewOpened] = useState(false);
    const [viewLocation, setViewLocation] = useState(null);

    const [loading, setLoading] = useState(true); // Add a loading state
    const [submitting, setSubmitting] = useState(false); // New state for tracking API call

    const [newLocation, setNewLocation] = useState({
        name: "",
        latitude: "",
        longitude: "",
        address: "",
        type: ""
    });

    useEffect(() => {
        getLocationFn()
    }, []);

    const getLocationFn = () => {

        getLocation({})
            .then((response) => {
                setLocations(response.data);
            })
            .catch((error) => {
                toast.error(error.response);
            }).finally(() => {

            setLoading(false); // Stop loading
        })
    }


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

        setSubmitting(true); // Disable button and show loader
        try {

            insertLocation(newLocation)
                .then((response) => {

                    toast.success(Constants.TOASTS.SUCCESS.LOCATION_CREATION_SUCCESS);

                    setModalOpened(false);
                    setNewLocation({
                        name: "",
                        latitude: "",
                        longitude: "",
                        address: "",
                        type: ""
                    })
                    getLocationFn()
                })
                .catch((error) => {
                    toast.error(error.response);
                }).finally(() => {

                setSubmitting(false); // Disable button and show loader
            })
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

                    <FormControl fullWidth margin="normal">
                        <InputLabel>Location</InputLabel>
                        <Select name="type" onChange={handleInputChange} required>
                            <MenuItem value={"TRIP_START"}>Trip Start</MenuItem>
                            <MenuItem value={"TRIP_END"}>Trip End</MenuItem>
                            <MenuItem value={"FUELING"}>Fueling</MenuItem>
                            <MenuItem value={"BREAK_REST"}>Break Rest</MenuItem>
                        </Select>
                    </FormControl>


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
                            disabled={(!newLocation.latitude || !newLocation.longitude)||submitting} // Disable until location is selected
                        >

                            {submitting ? <><CircularProgress size={10} sx={{color: "#1976d2"}}/> Save</> : "Save"}
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

            {loading ? (
                    <Box display="flex" flexDirection="column" alignItems="center">
                        <CircularProgress/>
                        <Typography variant="body2" sx={{mt: 2}}>Loading trips...</Typography>
                    </Box>
                ) :
                (
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

                )
            }
        </Container>
    );
}

export default Locations;
