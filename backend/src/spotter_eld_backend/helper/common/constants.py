class ResponseStatus:
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class RequestTypes:
    POST = "POST"
    PUT = "PUT"
    GET = "GET"
    DELETE = "DELETE"


class ResponseMessage:
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class Language:
    ENGLISH = "English"
    ARABIC = "Arabic"
    FRENCH = "French"
    PORTUGUESE = "Portuguese"
    SPANISH = "Spanish"


class Role:
    CREATOR = 'CREATOR'
    ADMIN = 'ADMIN'
    USER = 'USER'


class TripStatus:
    ONGOING = "ONGOING"
    ENDED = "ENDED"


class LocationType:
    TRIP_START = "TRIP_START"
    TRIP_END = "TRIP_END"
    BREAK_REST = "BREAK_REST"
    FUELING = "FUELING"
