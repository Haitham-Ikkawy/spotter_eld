import {createContext, useContext, useEffect, useState} from "react";
import {useMediaQuery, useTheme} from "@mui/material";

const LandingContext = createContext();

export const LandingContextProvider = ({children}) => {

    const theme = useTheme();

    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    // Initialize isAuth from localStorage
    const [isAuth, setIsAuth] = useState(() => !!localStorage.getItem("access_token"));

    useEffect(() => {
        setIsAuth(!!localStorage.getItem("access_token"));
    }, []);

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setIsAuth(false);
    };

    return (
        <LandingContext.Provider value={{isAuth, setIsAuth, logout, isMobile}}>
            {children}
        </LandingContext.Provider>
    );
};

export const useLanding = () => useContext(LandingContext);
