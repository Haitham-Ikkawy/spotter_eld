import React, {useEffect, useState} from "react";
import {Box, Button, Container, FormControl, InputLabel, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField} from "@mui/material";
import PageTitle from "../components/shared/PageTitle.jsx";
import {GetFueling, GetFuelingFormData, insertFueling} from "../services/Api.js";
import {toast} from "react-toastify";
import ModalLayout from "../components/modals/ModalLayout.jsx";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import Constants from "../common/constants.js";

function Fuelings() {

    const [fuelings, setFuelings] = useState([]);
    const [modalOpened, setModalOpened] = useState(false);
    const [locations, setLocations] = useState([]);
    const [trips, setTrips] = useState([]);
    const MAX_HOURS = 70;

    const [newFueling, setNewFueling] = useState({
        trip: "",
        location: "",
        amount: "",
        cost: "",
        mileage_at_fueling: "",
    });

    // Fetch fuelings from the backend
    useEffect(() => {
        getFuelingFn()
    }, []);


    useEffect(() => {
        if (modalOpened) {
            GetFuelingFormData({})
                .then((response) => {
                    setTrips(response.data.trips)
                    setLocations(response.data.locations)
                })
                .catch((error) => toast.error(error.response));
        }
    }, [modalOpened]);


    const getFuelingFn = () => {
        GetFueling({})
            .then((response) => {
                setFuelings(response.data);
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
                    setNewFueling((prev) => ({...prev, start_location: location}));
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
        setNewFueling({...newFueling, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (newFueling.current_cycle_used >= MAX_HOURS) {
            toast.error(Constants.TOASTS.ERROR.DRIVERS_HOUR_LIMIT_EXCEEDED);
            return;
        }

        try {
            insertFueling(newFueling)
                .then((response) => {
                    toast.success(Constants.TOASTS.SUCCESS.FUEL_STOP_CREATION_SUCCESS);

                    setModalOpened(false);
                    getFuelingFn()
                })
                .catch((error) => {
                    toast.error(error.response);
                });
        } catch (error) {
            toast.error(Constants.TOASTS.ERROR.FUEL_STOP_CREATION_FAILED);
        }
    };

    return (
        <Container>
            <PageTitle title="Fuelings"/>
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
            <ModalLayout title={"New Fueling Stop"} modalOpened={modalOpened} setModalOpened={setModalOpened}>

                <Box component="form" onSubmit={handleSubmit}>


                    <FormControl fullWidth margin="normal">
                        <InputLabel>Trip</InputLabel>
                        <Select name="trip" value={newFueling.trip} onChange={handleInputChange} required>
                            {trips.map((trip) => (
                                <MenuItem key={trip.id} value={trip.id}>
                                    {trip.driver.name} / {trip.start_dt}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>


                    <FormControl fullWidth margin="normal">
                        <InputLabel>Location</InputLabel>
                        <Select name="location" value={newFueling.location} onChange={handleInputChange} required>
                            {locations.map((location) => (
                                <MenuItem key={location.id} value={location.id}>
                                    {location.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* Current Cycle Used */}
                    <TextField type="number"
                        // inputProps={{min: 0, max: 100}} // Sets UI constraints
                               label="amount" name="amount" value={newFueling.amount} onChange={handleInputChange} fullWidth margin="normal" required/>


                    <TextField type="number"
                        // inputProps={{min: 0, max: 100}} // Sets UI constraints
                               label="cost" name="cost" value={newFueling.cost} onChange={handleInputChange} fullWidth margin="normal" required/>


                    <TextField type="number"
                        // inputProps={{min: 0, max: 100}} // Sets UI constraints
                               label="current mileage" name="mileage_at_fueling" value={newFueling.mileage_at_fueling} onChange={handleInputChange} fullWidth margin="normal" required/>

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
                            <TableCell>Amount</TableCell>
                            <TableCell>Cost</TableCell>
                            <TableCell>Milage</TableCell>
                            <TableCell>Date</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {fuelings.map(fueling => (
                            <TableRow key={fueling.id}>
                                <TableCell>{fueling.id}</TableCell>
                                <TableCell>{fueling.trip.id}</TableCell>
                                <TableCell>{fueling.location.name}</TableCell>
                                <TableCell>{fueling.amount}</TableCell>
                                <TableCell>{fueling.cost}</TableCell>
                                <TableCell>{fueling.mileage_at_fueling}</TableCell>
                                <TableCell>{fueling.created_dt}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

        </Container>
    );
}

export default Fuelings;
