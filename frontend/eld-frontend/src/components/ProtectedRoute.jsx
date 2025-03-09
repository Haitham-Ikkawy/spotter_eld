import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import Constants from "../common/constants.js";

const ProtectedRoute = () => {
  const token = localStorage.getItem("access_token");
  return token ? <Outlet /> : <Navigate to={Constants.ROUTES.LOGIN}/>;
};

export default ProtectedRoute;
