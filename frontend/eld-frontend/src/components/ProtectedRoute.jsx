import React from "react";
import {Navigate, Outlet} from "react-router-dom";

import {Box, useMediaQuery, useTheme} from '@mui/material';
import Constants from "../common/constants.js";
import {useLanding} from "../contexts/LandingContext.jsx";

const ProtectedRoute = () => {

    const {isMobile} = useLanding(); // Get authentication state
    const token = localStorage.getItem("access_token");
    const mainBoxStyle = isMobile ? {} : {display: "flex"}
    const nestedBoxStyle = isMobile ? {} : {flexGrow: 1, ml: 20, p: 3}
    return token ?
        <Box sx={mainBoxStyle}>
            <Box component="main" sx={nestedBoxStyle}>
                <Outlet/>
            </Box>
        </Box> :
        <Navigate to={Constants.ROUTES.LOGIN}/>;
};

export default ProtectedRoute;
