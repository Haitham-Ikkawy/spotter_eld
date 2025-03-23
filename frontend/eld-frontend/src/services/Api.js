import ApiRequest from "../config/ApiRequest";
import Tools from "../config/Tools.js";
import Constants from "../common/constants";

const LoginAPI = async (data) => {
    return ApiRequest.post(Constants.API_URLS.LOGIN, Tools.formData(data));
};

const GetTrips = async (data) => {
    return ApiRequest.get(Tools.buildGetURL(Constants.API_URLS.GET_TRIPS, data));
};

const GetTripTrace = async (data) => {
    return ApiRequest.get(Tools.buildGetURL(Constants.API_URLS.GET_TRIP_TRACE, data));
};

const GetTripsFormData = async (data) => {
    return ApiRequest.get(Constants.API_URLS.GET_TRIP_FORM_DATA);
};


const GetDriverLogSheet = async (data) => {
    return ApiRequest.get(Tools.buildGetURL(Constants.API_URLS.GET_DRIVER_LOG_SHEET, data));
};

const insertTrips = async (data) => {
    return ApiRequest.post(Constants.API_URLS.CREATE_TRIP, Tools.formData(data));
};


const canCreateTrip = async (data) => {
    return ApiRequest.post(Constants.API_URLS.CAN_CREATE_TRIP, Tools.formData(data));
};
const startPickup = async (data) => {
    return ApiRequest.post(Constants.API_URLS.START_PICKUP, Tools.formData(data));
};

const endPickup = async (data) => {
    return ApiRequest.post(Constants.API_URLS.END_PICKUP, Tools.formData(data));
};

const startDropOff = async (data) => {
    return ApiRequest.post(Constants.API_URLS.START_DROP_OFF, Tools.formData(data));
};
const endDropOff = async (data) => {
    return ApiRequest.post(Constants.API_URLS.END_DROP_OFF, Tools.formData(data));
};

const GetFueling = async (data) => {
    return ApiRequest.get(Tools.buildGetURL(Constants.API_URLS.GET_FUELING, data));
};

const GetFuelingFormData = async (data) => {
    return ApiRequest.get(Constants.API_URLS.GET_FUELING_FORM_DATA);
};

const insertFueling = async (data) => {
    return ApiRequest.post(Constants.API_URLS.CREATE_FUELING, Tools.formData(data));
};


const GetRestBreak = async (data) => {
    return ApiRequest.get(Tools.buildGetURL(Constants.API_URLS.GET_REST_BREAK, data));
};

const GetRestBreakFormData = async (data) => {
    return ApiRequest.get(Constants.API_URLS.GET_REST_BREAK_FORM_DATA);
};

const endRestBreak = async (data) => {
    return ApiRequest.post(Constants.API_URLS.END_REST_BREAK, Tools.formData(data));
};

const insertRestBreak = async (data) => {
    return ApiRequest.post(Constants.API_URLS.CREATE_REST_BREAK, Tools.formData(data));
};

const getLocation = async (data) => {
    return ApiRequest.get(Constants.API_URLS.GET_LOCATIONS, Tools.formData(data));
};
const insertLocation = async (data) => {
    return ApiRequest.post(Constants.API_URLS.CREATE_LOCATIONS, Tools.formData(data));
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
    canCreateTrip,
    insertTrips,
    startPickup,
    endPickup,
    startDropOff,
    endDropOff,
    insertLocation,
    getLocation,
    GetDriver,
    GetVehicles,
    GetFueling,
    GetFuelingFormData,
    insertFueling,
    GetRestBreak,
    GetRestBreakFormData,
    insertRestBreak,
    endRestBreak,
    GetTripTrace,
    GetDriverLogSheet
};