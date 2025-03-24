import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    CircularProgress,
    Container,
    FormControl,
    IconButton,
    Menu,
    MenuItem,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import {canCreateTrip, endDropOff, endPickup, GetTrips, GetTripsFormData, GetTripTrace, insertTrips, startDropOff, startPickup} from "../services/Api.js";
import {toast} from "react-toastify";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import Constants from "../common/constants.js";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import MapIcon from '@mui/icons-material/Map';

import * as PropTypes from "prop-types";
import TripMapTrace from "../components/modals/TripMapTrace.jsx";
import {Autocomplete} from "@mui/lab";

function FlightTakeoffIcon(props) {
    return null;
}

FlightTakeoffIcon.propTypes = {sx: PropTypes.shape({mr: PropTypes.number})};

function FlagIcon(props) {
    return null;
}

FlagIcon.propTypes = {sx: PropTypes.shape({mr: PropTypes.number})};

function Trips() {

    const [trips, setTrips] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [mapTraceModalOpened, setMapTraceModalOpened] = useState(false);
    const [useManualLocation, setUseManualLocation] = useState(false);
    const [currentLocation, setCurrentLocation] = useState("");
    const [drivers, setDrivers] = useState([]);
    const [locations, setLocations] = useState([]);
    const [vehicles, setVehicles] = useState([]);
    const [currentCycleUsed, setCurrentCycleUsed] = useState(0);
    const [anchorEl, setAnchorEl] = useState(null);
    const [selectedTrip, setSelectedTrip] = useState(null);
    const [canDriverCreateTrips, setCanDriverCreateTrips] = useState(false);
    const [serverMapTrace, setServerMapTrace] = useState(null);
    const [loading, setLoading] = useState(true); // Add a loading state
    const [submitting, setSubmitting] = useState(false); // New state for tracking API call
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
        // canCreateTripFn()
    }, []);


    useEffect(() => {
        if (modalOpened) {
            GetTripsFormData({})
                .then((response) => {
                    setDrivers(response.data.drivers)
                    setLocations(response.data.locations)
                    setVehicles(response.data.vehicles)
                    setCurrentCycleUsed(response.data.current_cycle_used)

                })
                .catch((error) => toast.error(error.response));
        }
    }, [modalOpened]);


    useEffect(() => {
        if (mapTraceModalOpened) {
            GetTripsFormData({})
                .then((response) => {
                    setDrivers(response.data.drivers)
                    setLocations(response.data.locations)
                    setVehicles(response.data.vehicles)
                    setCurrentCycleUsed(response.data.current_cycle_used)

                })
                .catch((error) => toast.error(error.response));
        }
    }, [mapTraceModalOpened]);
    const canCreateTripFn = () => {
        canCreateTrip({})
            .then((response) => {
                setCanDriverCreateTrips(response.data.can_create_trip);
                setModalOpened(true)
            })
            .catch((error) => {
                // toast.error(error.response);
            });

    }
    const getTripsFn = () => {
        GetTrips({})
            .then((response) => {
                setTrips(response.data);
            })
            .catch((error) => {
                // toast.error(error.response);
            }).finally(() => {

            setLoading(false); // Stop loading
        })

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


        setSubmitting(true); // Disable button and show loader

        // try {
        insertTrips(newTrip)
            .then((response) => {
                toast.success(Constants.TOASTS.SUCCESS.TRIP_CREATION_SUCCESS);
                setModalOpened(false);
                setNewTrip({
                    driver: "",
                    vehicle: "",
                    start_location: "",
                    end_location: "",
                    distance: "",
                    current_cycle_used: 0,
                })
                getTripsFn()

            })
            .catch((error) => {
                toast.error(error.response);
            }).finally(() => {

            setSubmitting(false); // Disable button and show loader
        })
        //
        // } catch (error) {
        //     toast.error(Constants.TOASTS.ERROR.TRIP_CREATION_FAILED);
        // }
    };
    const handleMenuClick = (event, trip) => {
        setAnchorEl(event.currentTarget);
        setSelectedTrip(trip);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
        setSelectedTrip(null);
    };

    const handleAction = async (action) => {
        if (!selectedTrip) return;
        try {
            if (action === "startPickup") {
                startPickup(selectedTrip)
                    .then((response) => {
                        toast.success(Constants.TOASTS.SUCCESS.PICKUP_STARTED_SUCCESSFULLY);
                        getTripsFn()
                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
            } else if (action === "endPickup") {
                endPickup(selectedTrip)
                    .then((response) => {
                        toast.success(Constants.TOASTS.SUCCESS.PICKUP_ENDED_SUCCESSFULLY);
                        getTripsFn()
                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
                // toast.success("Pickup ended successfully");
            } else if (action === "startDropoff") {
                startDropOff(selectedTrip)
                    .then((response) => {
                        toast.success(Constants.TOASTS.SUCCESS.DROP_OFF_STARTED_SUCCESSFULLY);
                        getTripsFn()
                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
            } else if (action === "endDropoff") {
                endDropOff(selectedTrip)
                    .then((response) => {
                        toast.success(Constants.TOASTS.SUCCESS.DROP_OFF_ENDED_SUCCESSFULLY);
                        getTripsFn()
                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
            } else if (action === "viewMapTrace") {
                setMapTraceModalOpened(true)
                GetTripTrace(selectedTrip)
                    .then((response) => {

                        setServerMapTrace(response.data)

                    })
                    .catch((error) => {
                        toast.error(error.response);
                    });
            }
            getTripsFn(); // Refresh trip list
        } catch (error) {
            toast.error("Action failed");
        }
        handleMenuClose();
    };

    return (
        <Container>
            <PageTitle title="Trips"/>
            <Box display="flex" justifyContent="flex-end" my={2}>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddCircleIcon/>}
                    onClick={() => {
                        canCreateTripFn()
                    }}
                >
                    Start NEW
                </Button>
            </Box>

            {canDriverCreateTrips &&
                <ModalLayout title={"New Trip"} modalOpened={modalOpened} setModalOpened={setModalOpened}>

                    <Box component="form" onSubmit={handleSubmit}>
                        {/*/!* Driver Selection *!/*/}
                        {/*<FormControl fullWidth margin="normal">*/}
                        {/*    <InputLabel>Driver</InputLabel>*/}
                        {/*    <Select name="driver" value={newTrip.driver} onChange={handleInputChange} required>*/}
                        {/*        {drivers.map((driver) => (*/}
                        {/*            <MenuItem key={driver.id} value={driver.id}>*/}
                        {/*                {driver.name} (Used: {driver.current_cycle_used} hrs)*/}
                        {/*            </MenuItem>*/}
                        {/*        ))}*/}
                        {/*    </Select>*/}
                        {/*</FormControl>*/}


                        {/* Vehicle Selection */}
                        <FormControl fullWidth margin="normal">
                            <Autocomplete
                                options={vehicles}
                                getOptionLabel={(option) => `${option.name} / ${option.model} / ${option.year}`}
                                renderInput={(params) => <TextField {...params} label="Vehicle" variant="outlined" required/>}
                                value={vehicles.find((v) => v.id === newTrip.vehicle) || null}
                                onChange={(event, newValue) => setNewTrip({...newTrip, vehicle: newValue ? newValue.id : ""})}

                            />
                            {/*<InputLabel>Vehicle</InputLabel>*/}
                            {/*<Select name="vehicle" value={newTrip.vehicle} onChange={handleInputChange} required>*/}
                            {/*    {vehicles.map((vehicle) => (*/}
                            {/*        <MenuItem key={vehicle.id} value={vehicle.id}>*/}
                            {/*            {vehicle.name} / {vehicle.model} / {vehicle.year}*/}
                            {/*        </MenuItem>*/}
                            {/*    ))}*/}
                            {/*</Select>*/}
                        </FormControl>

                        {/*/!* Current Location *!/*/}

                        <FormControl fullWidth margin="normal">

                            {/*// Start Location Selection*/}
                            <Autocomplete
                                options={locations}
                                getOptionLabel={(option) => option.name}
                                renderInput={(params) => <TextField {...params} label="Start Location" variant="outlined" required/>}
                                value={locations.find((l) => l.id === newTrip.start_location) || null}
                                onChange={(event, newValue) => setNewTrip({...newTrip, start_location: newValue ? newValue.id : ""})}
                            />
                            {/*<InputLabel>Start Location</InputLabel>*/}
                            {/*<Select name="start_location" value={newTrip.start_location} onChange={handleInputChange} required>*/}
                            {/*    {locations.map((location) => (*/}
                            {/*        <MenuItem key={location.id} value={location.id}>*/}
                            {/*            {location.name}*/}
                            {/*        </MenuItem>*/}
                            {/*    ))}*/}
                            {/*</Select>*/}
                        </FormControl>

                        {/* end_location Selection */}
                        <FormControl fullWidth margin="normal">
                            {/*<InputLabel>End Location</InputLabel>*/}
                            {/*<Select name="end_location" value={newTrip.end_location} onChange={handleInputChange} required>*/}
                            {/*    {locations.map((location) => (*/}
                            {/*        <MenuItem key={location.id} value={location.id}>*/}
                            {/*            {location.name}*/}
                            {/*        </MenuItem>*/}
                            {/*    ))}*/}
                            {/*</Select>*/}


                            {/*// End Location Selection*/}
                            <Autocomplete
                                options={locations}
                                getOptionLabel={(option) => option.name}
                                renderInput={(params) => <TextField {...params} label="End Location" variant="outlined" required/>}
                                value={locations.find((l) => l.id === newTrip.end_location) || null}
                                onChange={(event, newValue) => setNewTrip({...newTrip, end_location: newValue ? newValue.id : ""})}
                            />
                        </FormControl>

                        {/* Current Cycle Used */}
                        <TextField type="number"
                            // inputProps={{min: 0, max: 100}} // Sets UI constraints
                                   label="Distance" name="distance" value={newTrip.distance} onChange={handleInputChange} fullWidth margin="normal" required/>
                        {/* Current Cycle Used */}
                        <TextField label="Current Cycle Used (Hrs)" name="current_cycle_used" value={currentCycleUsed} onChange={handleInputChange} fullWidth margin="normal" required
                                   disabled/>

                        <Button type="submit" variant="contained" color="primary" sx={{mt: 2}} disabled={submitting}>
                            {submitting ? <><CircularProgress size={10} sx={{color: "#1976d2"}}/> Start Trip</> : "Start Trip"}
                        </Button>
                    </Box>
                </ModalLayout>
            }

            {serverMapTrace &&

                <ModalLayout title={"Map Trace Modal"} modalOpened={mapTraceModalOpened} setModalOpened={setMapTraceModalOpened}>

                    <TripMapTrace tripTrace={serverMapTrace}/>
                </ModalLayout>
            }
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
                                        <TableCell>{trip.start_location.name}</TableCell>
                                        <TableCell>{trip.end_location.name}</TableCell>
                                        <TableCell>{trip.start_dt}</TableCell>
                                        <TableCell>{trip.end_dt}</TableCell>
                                        <TableCell>{trip.distance}</TableCell>
                                        <TableCell>
                                            <IconButton onClick={(e) => handleMenuClick(e, trip)}>
                                                <MoreVertIcon/>
                                            </IconButton>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>


                        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
                            {selectedTrip?.show_start_pickup && (
                                <MenuItem onClick={() => handleAction("startPickup")}>
                                    <LocalShippingIcon sx={{mr: 1}}/> Start Pickup
                                </MenuItem>
                            )}


                            {selectedTrip?.show_end_pickup && (
                                <MenuItem onClick={() => handleAction("endPickup")}>
                                    <LocalShippingIcon sx={{mr: 1}}/> End Pickup
                                </MenuItem>
                            )}
                            {selectedTrip?.show_start_drop_off && (
                                <MenuItem onClick={() => handleAction("startDropoff")}>
                                    <FlightTakeoffIcon sx={{mr: 1}}/> Start Dropoff
                                </MenuItem>
                            )}
                            {selectedTrip?.show_end_drop_off && (
                                <MenuItem onClick={() => handleAction("endDropoff")}>
                                    <FlagIcon sx={{mr: 1}}/> End Dropoff
                                </MenuItem>
                            )}

                            <MenuItem onClick={() => handleAction("viewMapTrace")}>
                                <MapIcon sx={{mr: 1}}/> View Map Trace
                            </MenuItem>
                        </Menu>
                    </TableContainer>
                )
            }

        </Container>
    );
}

export default Trips;
