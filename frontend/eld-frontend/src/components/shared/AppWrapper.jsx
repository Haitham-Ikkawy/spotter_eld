import {ToastContainer} from "react-toastify";
import {BrowserRouter as Router, Navigate, Route, Routes} from "react-router-dom";
import Navbar from "../Navbar.jsx";
import Login from "../../pages/Login.jsx";
import {useLanding} from "../../contexts/LandingContext.jsx";
import Constants from "../../common/constants.js";
import ProtectedRoute from "../ProtectedRoute.jsx";
import Dashboard from "../../pages/Dashboard.jsx";
import Locations from "../../pages/Locations.jsx";
import Trips from "../../pages/Trips.jsx";
import Breaks from "../../pages/Breaks.jsx";
import Fuelings from "../../pages/Fuelings.jsx";
import RestBreaks from "../../pages/RestBreaks.jsx";
import DriverLogSheet from "../../pages/DriverLogSheet.jsx";

const AppRoutes = () => {
    const {isAuth} = useLanding(); // Get authentication state

    return (
        <>

            <ToastContainer autoClose={3000} closeOnClick/>
            {isAuth && <Navbar/>}


            <Routes>
                {/* Default route: If not authenticated, go to login */}
                <Route path={Constants.ROUTES.LOGIN} element={isAuth ? <Navigate to={Constants.ROUTES.DASHBOARD}/> : <Login/>}/>

                {/* Authenticated Routes */}
                {isAuth && (
                    <Route element={<ProtectedRoute/>}>
                        <Route path={Constants.ROUTES.DASHBOARD} element={<Dashboard/>}/>
                        <Route path={Constants.ROUTES.TRIPS} element={<Trips/>}/>
                        <Route path={Constants.ROUTES.LOCATIONS} element={<Locations/>}/>
                        <Route path={Constants.ROUTES.BREAKS} element={<RestBreaks/>}/>
                        <Route path={Constants.ROUTES.FUELING} element={<Fuelings/>}/>
                        <Route path={Constants.ROUTES.LOG_SHEET} element={<DriverLogSheet/>}/>
                        {/*<Route path="/driver-logs" element={<DriverLogs/>}/>*/}
                        {/*<Route path="/vehicles" element={<Vehicles/>}/>*/}
                        {/*<Route path="/rest-breaks" element={<RestBreaks/>}/>*/}
                        {/*<Route path="/fueling-stops" element={<FuelingStops/>}/>*/}
                    </Route>
                )}

                {/* Catch-All Route */}
                <Route path="*" element={<Navigate to={isAuth ? Constants.ROUTES.DASHBOARD : Constants.ROUTES.LOGIN}/>}/>
            </Routes>
        </>
    );
};

const AppWrapper = () => {
    return (
        <>
            <ToastContainer autoClose={3000} closeOnClick/>
            <Router>
                <AppRoutes/>
            </Router>
        </>
    );
};

export default AppWrapper;
