export default {
    TOASTS: {
        SUCCESS: {
            TRIP_CREATION_SUCCESS: "Trip started successfully"
        },
        ERROR: {
            UNKNOWN_ERROR: "UNKNOWN_ERROR",
            LOCATION_DETECTION_FAILED: "Failed to detect location",
            GEOLOCATION_NOT_SUPPORTED: "Geolocation is not supported by this browser",
            DRIVERS_HOUR_LIMIT_EXCEEDED: "Driver has exceeded the 70-hour limit. Trip cannot be started.",
            TRIP_CREATION_FAILED: "Error starting trip"
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
        // LOGIN: "/",
    },

    API_URLS: {
        LOGIN: "token/",
        TRIPS: "trips/",
        TRIPS_FORM_DATA: "trip_form_data",
        LOCATIONS: "locations/",
        DRIVERS: "drivers/",
        VEHICLES: "Vehicles/",
    }
}