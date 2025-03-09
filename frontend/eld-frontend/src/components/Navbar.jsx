import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import {AppBar, Button, IconButton, Menu, MenuItem, Toolbar, Typography, useMediaQuery, useTheme} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Constants from "../common/constants.js";
import {useLanding} from "../contexts/LandingContext.jsx";

function Navbar() {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const [anchorEl, setAnchorEl] = useState(null);

    const {logout} = useLanding(); // Get login function and user state

    const handleMenuOpen = (event) => setAnchorEl(event.currentTarget);
    const handleMenuClose = () => setAnchorEl(null);

    const handleLogout = () => {
        logout()
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
                    ELD App
                </Typography>

                {!isMobile ? (
                    <>
                        <Button color="inherit" component={Link} to={Constants.ROUTES.DASHBOARD}>Dashboard</Button>
                        <Button color="inherit" component={Link} to={Constants.ROUTES.TRIPS}>Trips</Button>
                        <Button color="inherit" component={Link} to={Constants.ROUTES.LOCATIONS}>Locations</Button>
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.}     >Trips</Button>*/}
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.}     >Driver Logs</Button>*/}
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.} >Vehicles</Button>*/}
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.}         >Locations</Button>*/}
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.}         >Rest Breaks</Button>*/}
                        {/*<Button color="inherit" component={Link} to={Constants.ROUTES.}       >Fueling Stops</Button>*/}
                        <Button color="inherit" onClick={handleLogout}>Logout</Button>
                    </>
                ) : (
                    <>
                        <IconButton color="inherit" onClick={handleMenuOpen}>
                            <MenuIcon/>
                        </IconButton>
                        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
                            <MenuItem onClick={handleMenuClose} component={Link} to={Constants.ROUTES.DASHBOARD}>Dashboard</MenuItem>
                            <MenuItem onClick={handleMenuClose} component={Link} to={Constants.ROUTES.TRIPS}>Trips</MenuItem>
                            <MenuItem onClick={handleMenuClose} component={Link} to={Constants.ROUTES.LOCATIONS}>Locations</MenuItem>


                            {/*<MenuItem onClick={handleMenuClose} component={Link} to="/driver-logs">Driver Logs</MenuItem>*/}
                            {/*<MenuItem onClick={handleMenuClose} component={Link} to="/vehicles">Vehicles</MenuItem>*/}
                            {/*<MenuItem onClick={handleMenuClose} component={Link} to="/rest-breaks">Rest Breaks</MenuItem>*/}
                            {/*<MenuItem onClick={handleMenuClose} component={Link} to="/fueling-stops">Fueling Stops</MenuItem>*/}
                            <MenuItem onClick={handleLogout}>Logout</MenuItem>
                        </Menu>
                    </>
                )}
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;