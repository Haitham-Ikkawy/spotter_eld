import { createContext, useContext, useState, useEffect } from "react";

const LandingContext = createContext();

export const LandingContextProvider = ({ children }) => {
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
    <LandingContext.Provider value={{ isAuth, setIsAuth, logout }}>
      {children}
    </LandingContext.Provider>
  );
};

export const useLanding = () => useContext(LandingContext);
