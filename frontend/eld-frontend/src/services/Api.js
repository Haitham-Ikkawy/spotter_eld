import ApiRequest from "../config/ApiRequest";
import Tools from "../config/Tools.js";
import Constants from "../common/constants";

const LoginAPI = async (data) => {
    return ApiRequest.post(Constants.API_URLS.LOGIN, Tools.formData(data));
};

const GetTrips = async (data) => {
    return ApiRequest.get(Constants.API_URLS.TRIPS);
};

const GetTripsFormData = async (data) => {
    return ApiRequest.get(Constants.API_URLS.TRIPS_FORM_DATA);
};

const insertTrips = async (data) => {
    return ApiRequest.post(Constants.API_URLS.TRIPS, Tools.formData(data));
};

const getLocation = async (data) => {
    return ApiRequest.get(Constants.API_URLS.LOCATIONS, Tools.formData(data));
};
const insertLocation = async (data) => {
    return ApiRequest.post(Constants.API_URLS.LOCATIONS, Tools.formData(data));
};

const GetDriver = async (data) => {
    return ApiRequest.get(Constants.API_URLS.DRIVERS, Tools.formData(data));
};

const GetVehicles = async (data) => {
    return ApiRequest.get(Constants.API_URLS.VEHICLES, Tools.formData(data));
};


export {
    LoginAPI,
    GetTrips,
    GetTripsFormData,
    insertTrips,
    insertLocation,
    getLocation,
    GetDriver,
    GetVehicles
};