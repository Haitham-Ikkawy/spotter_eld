import React from 'react';
import {Typography, Container, Modal, Box, TextField, Button, TableContainer, Paper, Table, TableHead, TableRow, TableCell, TableBody} from '@mui/material';
import PageTitle from "../components/shared/PageTitle.jsx";

function Dashboard() {
  return (

        <Container>
            <PageTitle title="Dashboard"/>

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

                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
  );
}

export default Dashboard;