import React, {useEffect, useState} from "react";
import {Box, Button, Container, FormControl, IconButton, InputLabel, Menu, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import {GetRestBreak, GetRestBreakFormData, insertRestBreak, endRestBreak} from "../services/Api.js";
import {toast} from "react-toastify";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import Constants from "../common/constants.js";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import HotelIcon from "@mui/icons-material/Hotel";

function RestBreaks() {

    const [restBreaks, setRestBreak] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [locations, setLocations] = useState([]);
    const [trips, setTrips] = useState([]);

    const [anchorEl, setAnchorEl] = useState(null);

    const [selectedRestBreak, setSelectedRestBreak] = useState(null);
    const MAX_HOURS = 70;

    const [newRestBreak, setNewRestBreak] = useState({
        trip: "",
        location: "",
        duration: ""
    });

    // Fetch restBreaks from the backend
    useEffect(() => {
        getRestBreakFn()
    }, []);


    useEffect(() => {
        if (modalOpened) {
            GetRestBreakFormData({})
                .then((response) => {
                    setTrips(response.data.trips)
                    setLocations(response.data.locations)
                })
                .catch((error) => toast.error(error.response));
        }
    }, [modalOpened]);


    const getRestBreakFn = () => {
        GetRestBreak({})
            .then((response) => {
                setRestBreak(response.data);
            })
            .catch((error) => {
                // toast.error(error.response);
            });

    }
    const getGeoLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const location = `${position.coords.latitude}, ${position.coords.longitude}`;
                    setCurrentLocation(location);
                    setNewRestBreak((prev) => ({...prev, start_location: location}));
                },
                (error) => {
                    toast.error(Constants.TOASTS.ERROR.LOCATION_DETECTION_FAILED);
                }
            );
        } else {
            toast.error(Constants.TOASTS.ERROR.GEOLOCATION_NOT_SUPPORTED);
        }
    };

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setNewRestBreak({...newRestBreak, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            insertRestBreak(newRestBreak)
                .then((response) => {
                    toast.success(Constants.TOASTS.SUCCESS.REST_BREAK_CREATION_SUCCESS);

                    setModalOpened(false);
                    getRestBreakFn()
                })
                .catch((error) => {
                    toast.error(error.response);
                });
        } catch (error) {

            toast.error(Constants.TOASTS.ERROR.FUEL_STOP_CREATION_FAILED);
        }
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
        setSelectedRestBreak(null);
    };

    const handleAction = async (action) => {
        if (!selectedRestBreak) return;
        try {
            if (action === "endRestBreak") {
                endRestBreak(selectedRestBreak)
                    .then((response) => {
                        toast.success(Constants.TOASTS.SUCCESS.REST_BREAK_ENDED_SUCCESSFULLY);
                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
            }
            getRestBreakFn(); // Refresh trip list
        } catch (error) {
            toast.error("Action failed");
        }
        handleMenuClose();
    };

    const handleMenuClick = (event, restBreak) => {
        setAnchorEl(event.currentTarget);
        setSelectedRestBreak(restBreak);
    };


    return (
        <Container>
            <PageTitle title="Rest Breaks"/>
            <Box display="flex" justifyContent="flex-end" my={2}>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddCircleIcon/>}
                    onClick={() => setModalOpened(true)}
                >
                    Start NEW
                </Button>
            </Box>
            <ModalLayout title={"New Rest Break"} modalOpened={modalOpened} setModalOpened={setModalOpened}>

                <Box component="form" onSubmit={handleSubmit}>


                    <FormControl fullWidth margin="normal">
                        <InputLabel>Trip</InputLabel>
                        <Select name="trip" value={newRestBreak.trip} onChange={handleInputChange} required>
                            {trips.map((trip) => (
                                <MenuItem key={trip.id} value={trip.id}>
                                    {trip.driver.name} / {trip.start_dt}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>


                    <FormControl fullWidth margin="normal">
                        <InputLabel>Location</InputLabel>
                        <Select name="location" value={newRestBreak.location} onChange={handleInputChange} required>
                            {locations.map((location) => (
                                <MenuItem key={location.id} value={location.id}>
                                    {location.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>


                    <TextField type="number"
                        // inputProps={{min: 0, max: 100}} // Sets UI constraints
                               label="duration" name="duration" value={newRestBreak.duration} onChange={handleInputChange} fullWidth margin="normal" required/>

                    <Button type="submit" variant="contained" color="primary" sx={{mt: 2}}>
                        Add Fuel Stop
                    </Button>
                </Box>
            </ModalLayout>


            {/* Trips Table */}
            <TableContainer component={Paper} sx={{mt: 4}}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Trip</TableCell>
                            <TableCell>Location</TableCell>
                            <TableCell>Duration</TableCell>
                            <TableCell>Date</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {restBreaks.map(restBreak => (
                            <TableRow key={restBreak.id}>
                                <TableCell>{restBreak.id}</TableCell>
                                <TableCell>{restBreak.trip.id}</TableCell>
                                <TableCell>{restBreak.location.name}</TableCell>
                                <TableCell>{restBreak.duration} min</TableCell>
                                <TableCell>{restBreak.created_dt}</TableCell>
                                <TableCell>
                                    <IconButton onClick={(e) => handleMenuClick(e, restBreak)}>
                                        <MoreVertIcon/>
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>

                <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>

                    <MenuItem onClick={() => handleAction("endRestBreak")}>
                        <HotelIcon sx={{mr: 1}}/> End Rest Break
                    </MenuItem>

                </Menu>
            </TableContainer>

        </Container>
    );
}

export default RestBreaks;
