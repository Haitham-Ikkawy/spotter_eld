export default {
    LOCATIONS: {
        TYPES: {
            TRIP_START: "TRIP_START",
            TRIP_END: "TRIP_END",
            BREAK_REST: "BREAK_REST",
            FUELING: "FUELING",
        }
    },
    TOASTS: {
        SUCCESS: {
            TRIP_CREATION_SUCCESS: "Trip started successfully",
            FUEL_STOP_CREATION_SUCCESS: "Fueling Stop Added successfully",
            REST_BREAK_CREATION_SUCCESS: "Rest Break Added successfully",
            LOCATION_CREATION_SUCCESS: "Location Created Successfully",
            PICKUP_STARTED_SUCCESSFULLY:"Pickup started successfully",
            PICKUP_ENDED_SUCCESSFULLY:"Pickup ended successfully",
            DROP_OFF_STARTED_SUCCESSFULLY:"Drop off started successfully",
            DROP_OFF_ENDED_SUCCESSFULLY:"Drop off ended successfully",
            REST_BREAK_ENDED_SUCCESSFULLY:"Rest Break ended successfully"
        },
        ERROR: {
            UNKNOWN_ERROR: "UNKNOWN_ERROR",
            LOCATION_DETECTION_FAILED: "Failed to detect location",
            GEOLOCATION_NOT_SUPPORTED: "Geolocation is not supported by this browser",
            DRIVERS_HOUR_LIMIT_EXCEEDED: "Driver has exceeded the 70-hour limit. Trip cannot be started.",
            TRIP_CREATION_FAILED: "Error starting trip",
            FUEL_STOP_CREATION_FAILED: "FUEL_STOP_CREATION_FAILED"
        },
        WARNING: {}
    },
    ROUTES: {
        LOGIN: "/",
        DASHBOARD: "/dashboard",
        TRIPS: "/trips",
        LOCATIONS: "/locations",
        BREAKS: "/breaks",
        FUELING: "/fueling",
        LOG_SHEET: "/log_sheet",
        // LOGIN: "/",
    },

    API_URLS: {
        LOGIN: "token/",
        GET_TRIPS: "trips/get_trips",
        GET_TRIP_TRACE:"trips/get_trip_trace",
        GET_TRIP_FORM_DATA: "trips/get_trip_form_data",
        CREATE_TRIP: "trips/create_trip",
        UPDATE_TRIP: "trips/update_trip",
        CAN_CREATE_TRIP: "trips/can_create_trip",
        START_PICKUP: "trips/start_pickup",
        END_PICKUP: "trips/end_pickup",
        START_DROP_OFF:"trips/start_drop_off",
        END_DROP_OFF:"trips/end_drop_off",


        GET_LOCATIONS: "locations/get_locations",
        GET_LOCATIONS_FORM_DATA: "locations/get_location_form_data",
        CREATE_LOCATIONS: "locations/create_location",
        UPDATE_LOCATIONS: "locations/update_location",



        GET_FUELING: "fueling/get_fueling",
        GET_FUELING_FORM_DATA: "fueling/get_fueling_form_data",
        CREATE_FUELING: "fueling/create_fueling",
        UPDATE_FUELING: "fueling/update_fueling",


        GET_REST_BREAK: "rest_breaks/get_rest_break",
        GET_REST_BREAK_FORM_DATA: "rest_breaks/get_rest_break_form_data",
        CREATE_REST_BREAK: "rest_breaks/create_rest_break",
        UPDATE_REST_BREAK: "rest_breaks/update_rest_break",
        END_REST_BREAK:"rest_breaks/end_rest_break",

        GET_DRIVER_LOG_SHEET:"trips/get_driver_log_sheet"

        //
        // DRIVERS: "drivers/",
        // VEHICLES: "Vehicles/",
    }
}