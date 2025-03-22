

from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def driver_profile_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'driver_profile'):
            return Response(
                {"error": "Authenticated user is not associated with a driver profile"},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return wrapper
