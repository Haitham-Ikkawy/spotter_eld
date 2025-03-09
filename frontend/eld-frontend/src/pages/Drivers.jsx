import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box } from '@mui/material';

function Drivers() {
  const [drivers, setDrivers] = useState([]);
  const [newDriver, setNewDriver] = useState({
    name: '',
    licenseNumber: '',
    currentCycleUsed: 0,
  });

  // Fetch drivers from the backend
  useEffect(() => {
    axios.get('/api/drivers/')
      .then(response => setDrivers(response.data))
      .catch(error => console.error(error));
  }, []);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewDriver({ ...newDriver, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/drivers/', newDriver);
      setDrivers([...drivers, response.data]); // Add new driver to the list
      setNewDriver({ name: '', licenseNumber: '', currentCycleUsed: 0 }); // Reset form
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Drivers
      </Typography>

      {/* Add Driver Form */}
      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <TextField
          label="Name"
          name="name"
          value={newDriver.name}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="License Number"
          name="licenseNumber"
          value={newDriver.licenseNumber}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="Current Cycle Used (Hours)"
          name="currentCycleUsed"
          type="number"
          value={newDriver.currentCycleUsed}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
          required
        />
        <Button type="submit" variant="contained" color="primary">
          Add Driver
        </Button>
      </Box>

      {/* Drivers Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>License Number</TableCell>
              <TableCell>Current Cycle Used (Hours)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {drivers.map(driver => (
              <TableRow key={driver.id}>
                <TableCell>{driver.id}</TableCell>
                <TableCell>{driver.name}</TableCell>
                <TableCell>{driver.licenseNumber}</TableCell>
                <TableCell>{driver.currentCycleUsed}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default Drivers;