import React, {useEffect, useState} from "react";
import {Box, Button, Container, FormControl, InputLabel, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import {GetTrips, GetTripsFormData, insertTrips} from "../services/Api.js";
import {toast} from "react-toastify";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import Constants from "../common/constants.js";

function Trips() {

    const [trips, setTrips] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [useManualLocation, setUseManualLocation] = useState(false);
    const [currentLocation, setCurrentLocation] = useState("");
    const [drivers, setDrivers] = useState([]);
    const [locations, setLocations] = useState([]);
    const [vehicles, setVehicles] = useState([]);
    const MAX_HOURS = 70;

    const [newTrip, setNewTrip] = useState({
        driver: "",
        vehicle: "",
        start_location: "",
        end_location: "",
        distance: "",
        current_cycle_used: 0,
    });

    // Fetch trips from the backend
    useEffect(() => {
        getTripsFn()
    }, []);


    useEffect(() => {
        if (modalOpened) {
            GetTripsFormData({})
                .then((response) => {
                    setDrivers(response.data.drivers)
                    setLocations(response.data.locations)
                    setVehicles(response.data.vehicles)

                })
                .catch((error) => toast.error(error.response));
        }
    }, [modalOpened]);


    const getTripsFn = () => {
        GetTrips({})
            .then((response) => {
                setTrips(response.data);
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
                    setNewTrip((prev) => ({...prev, start_location: location}));
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
        setNewTrip({...newTrip, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (newTrip.current_cycle_used >= MAX_HOURS) {
            toast.error(Constants.TOASTS.ERROR.DRIVERS_HOUR_LIMIT_EXCEEDED);
            return;
        }

        try {
            insertTrips(newTrip)
                .then((response) => {
                    toast.success(Constants.TOASTS.SUCCESS.TRIP_CREATION_SUCCESS);
                    getTripsFn()
                })
                .catch((error) => {
                    toast.error(error.response);
                });
            setModalOpened(false);
        } catch (error) {
            toast.error(Constants.TOASTS.ERROR.TRIP_CREATION_FAILED);
        }
    };

    return (
        <Container>
            <PageTitle title="Trips"/>
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
            <ModalLayout title={"New Trip"} modalOpened={modalOpened} setModalOpened={setModalOpened}>

                <Box component="form" onSubmit={handleSubmit}>
                    {/* Driver Selection */}
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Driver</InputLabel>
                        <Select name="driver" value={newTrip.driver} onChange={handleInputChange} required>
                            {drivers.map((driver) => (
                                <MenuItem key={driver.id} value={driver.id}>
                                    {driver.name} (Used: {driver.current_cycle_used} hrs)
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>


                    {/* Vehicle Selection */}
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Vehicle</InputLabel>
                        <Select name="vehicle" value={newTrip.vehicle} onChange={handleInputChange} required>
                            {vehicles.map((vehicle) => (
                                <MenuItem key={vehicle.id} value={vehicle.id}>
                                    {vehicle.model}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/*/!* Current Location *!/*/}
                    {/*<Button onClick={getGeoLocation} variant="outlined" fullWidth>*/}
                    {/*    Auto-Detect Current Location*/}
                    {/*</Button>*/}

                    {/*<TextField label="start_location Location" name="start_location" value={useManualLocation ? newTrip.start_location : currentLocation} onChange={handleInputChange} fullWidth*/}
                    {/*           margin="normal" required disabled={!useManualLocation}/>*/}

                    {/*<TextField label="end_location Location" name="end_location" value={useManualLocation ? newTrip.end_location : currentLocation} onChange={handleInputChange} fullWidth*/}
                    {/*           margin="normal" required disabled={!useManualLocation}/>*/}


                    <Button onClick={() => {
                        useManualLocation ? getGeoLocation() : ""
                        setUseManualLocation(!useManualLocation)
                    }}>{useManualLocation ? "Use Auto-detect" : "Enter Manually"}</Button>
                    {/*/!* start_location Selection *!/*/}
                    {useManualLocation ?
                        <FormControl fullWidth margin="normal">
                            <InputLabel>Location</InputLabel>
                            <Select name="start_location" value={newTrip.start_location} onChange={handleInputChange} required>
                                {locations.map((location) => (
                                    <MenuItem key={location.id} value={location.id}>
                                        {location.name}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl> :

                        <TextField label="Pickup Location" name="start_location" value={newTrip.start_location} onChange={handleInputChange} fullWidth margin="normal" required/>

                    }
                    {/* end_location Selection */}
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Location</InputLabel>
                        <Select name="end_location" value={newTrip.end_location} onChange={handleInputChange} required>
                            {locations.map((location) => (
                                <MenuItem key={location.id} value={location.id}>
                                    {location.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* Pickup & Dropoff Locations */}
                    {/*<TextField label="Dropoff Location" name="end_location" value={newTrip.end_location} onChange={handleInputChange} fullWidth margin="normal" required/>*/}

                    {/* Current Cycle Used */}
                    <TextField type="number"
                               inputProps={{min: 0, max: 100}} // Sets UI constraints
                               label="Distance" name="distance" value={newTrip.distance} onChange={handleInputChange} fullWidth margin="normal" required/>
                    {/* Current Cycle Used */}
                    <TextField label="Current Cycle Used (Hrs)" name="current_cycle_used" value={newTrip.current_cycle_used} onChange={handleInputChange} fullWidth margin="normal" required
                               disabled/>

                    <Button type="submit" variant="contained" color="primary" sx={{mt: 2}}>
                        Start Trip
                    </Button>
                </Box>
            </ModalLayout>


            {/* Trips Table */}
            <TableContainer component={Paper} sx={{mt: 4}}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Driver</TableCell>
                            <TableCell>Vehicle</TableCell>
                            <TableCell>Start Location</TableCell>
                            <TableCell>End Location</TableCell>
                            <TableCell>Start Time</TableCell>
                            <TableCell>End Time</TableCell>
                            <TableCell>Distance (Miles)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {trips.map(trip => (
                            <TableRow key={trip.id}>
                                <TableCell>{trip.id}</TableCell>
                                <TableCell>{trip.driver.name}</TableCell>
                                <TableCell>{trip.vehicle.model}</TableCell>
                                <TableCell>{trip.start_location}</TableCell>
                                <TableCell>{trip.end_location}</TableCell>
                                <TableCell>{trip.start_time}</TableCell>
                                <TableCell>{trip.end_time}</TableCell>
                                {/*<TableCell>{trip.distance}</TableCell>*/}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

        </Container>
    );
}

export default Trips;
