import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Menu,
    MenuItem,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    useMediaQuery,
    useTheme,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import LocalGasStationIcon from '@mui/icons-material/LocalGasStation';
import HotelIcon from '@mui/icons-material/Hotel';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import Constants from '../common/constants.js';
import { useLanding } from '../contexts/LandingContext.jsx';

function Navbar() {
    const theme = useTheme();

    const {isMobile} = useLanding(); // Get authentication state
    const [mobileMenuAnchor, setMobileMenuAnchor] = useState(null);
    const { logout } = useLanding();
    const location = useLocation();

    const handleMobileMenuOpen = (event) => setMobileMenuAnchor(event.currentTarget);
    const handleMobileMenuClose = () => setMobileMenuAnchor(null);

    const handleLogout = () => {
        logout();
        handleMobileMenuClose();
    };

    const isActive = (path) => location.pathname === path;

    // Custom styles
    const sidebarStyle = {
        width: 250,
        backgroundColor: theme.palette.grey[900], // Dark background for sidebar
        color: theme.palette.common.white, // White text
    };

    const titleStyle = {
        backgroundColor: theme.palette.primary.dark,
        color: theme.palette.common.white,
        padding: theme.spacing(2),
        textAlign: 'center',
    };

    const activeStyle = {
        backgroundColor: theme.palette.primary.light,
        color: theme.palette.primary.contrastText,
        borderRadius: '4px',
    };

    const menuItems = [
        { text: 'Dashboard', icon: <DashboardIcon />, path: Constants.ROUTES.DASHBOARD },
        { text: 'Trips', icon: <LocalShippingIcon />, path: Constants.ROUTES.TRIPS },
        { text: 'Locations', icon: <LocationOnIcon />, path: Constants.ROUTES.LOCATIONS },
        { text: 'Fueling Stops', icon: <LocalGasStationIcon />, path: Constants.ROUTES.FUELING },
        { text: 'Rest Breaks', icon: <HotelIcon />, path: Constants.ROUTES.BREAKS },
    ];

    return (
        <>
            {/* Sidebar for Desktop */}
            {!isMobile && (
                <Drawer
                    variant="permanent"
                    sx={{
                        width: 250,
                        flexShrink: 0,
                        '& .MuiDrawer-paper': {
                            width: 250,
                            boxSizing: 'border-box',
                            ...sidebarStyle, // Sidebar background color
                        },
                    }}
                >
                    <div style={titleStyle}>
                        <Typography variant="h6">ELD App</Typography>
                    </div>
                    <List>

                        {menuItems.map((item) => (
                            <ListItem key={item.text} disablePadding>
                                <ListItemButton
                                    component={Link}
                                    to={item.path}
                                    sx={isActive(item.path) ? activeStyle : {}}
                                >
                                    <ListItemIcon sx={{ color: 'white' }}>{item.icon}</ListItemIcon>
                                    <ListItemText primary={item.text} />
                                </ListItemButton>
                            </ListItem>
                        ))}
                        <ListItem disablePadding>
                            <ListItemButton onClick={handleLogout}>
                                <ListItemIcon sx={{ color: 'white' }}>
                                    <ExitToAppIcon />
                                </ListItemIcon>
                                <ListItemText primary="Logout" />
                            </ListItemButton>
                        </ListItem>
                    </List>
                </Drawer>
            )}

            {/* Top Navbar for Mobile */}
            {isMobile && (
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            ELD App
                        </Typography>
                        <IconButton color="inherit" onClick={handleMobileMenuOpen}>
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            anchorEl={mobileMenuAnchor}
                            open={Boolean(mobileMenuAnchor)}
                            onClose={handleMobileMenuClose}
                        >
                            {menuItems.map((item) => (
                                <MenuItem
                                    key={item.text}
                                    onClick={handleMobileMenuClose}
                                    component={Link}
                                    to={item.path}
                                    sx={isActive(item.path) ? activeStyle : {}}
                                >
                                    {item.icon} <Typography sx={{ marginLeft: 1 }}>{item.text}</Typography>
                                </MenuItem>
                            ))}
                            <MenuItem onClick={handleLogout}>
                                <ExitToAppIcon sx={{ marginRight: 1 }} /> Logout
                            </MenuItem>
                        </Menu>
                    </Toolbar>
                </AppBar>
            )}
        </>
    );
}

export default Navbar;
