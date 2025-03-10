import React from 'react';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, ml: 30, p: 3 }}> {/* Adjust main content */}
        <Dashboard />
      </Box>
    </Box>
  );
}

export default App;
