# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views.eld import (
#     DriverViewSet, VehicleViewSet, LocationViewSet,
#     TripViewSet, DriverLogViewSet, RestBreakViewSet, FuelingViewSet
# )
# from .views.auth import login_user, register_user
#
# # Create a router and register viewsets
# router = DefaultRouter()
# router.register(r'drivers', DriverViewSet)
# router.register(r'vehicles', VehicleViewSet)
# router.register(r'locations', LocationViewSet)
# router.register(r'trips', TripViewSet)
# router.register(r'driver-logs', DriverLogViewSet)
# router.register(r'rest-breaks', RestBreakViewSet)
# router.register(r'fuelings', FuelingViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('login/', login_user, name="login"),
#     path('register/', register_user, name="register"),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import trip, fueling, rest_break, location
from .views.auth import login_user, register_user
from .views.eld import (
    driver_list, driver_detail, vehicle_list, vehicle_detail,
    location_list, location_detail, trip_list, trip_detail,
    driverlog_list, driverlog_detail, restbreak_list, restbreak_detail,
    fueling_list, trip_form_data
    # fueling_detail
)

urlpatterns = [

    # Trip Endpoints
    path('trips/', include(trip.urls)),
    # Trip Endpoints
    path('fueling/', include(fueling.urls)),
    path('rest_breaks/', include(rest_break.urls)),
    path('locations/', include(location.urls)),

    # path('', include(router.urls)),
    path('login/', login_user, name="login"),
    path('register/', register_user, name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Authentication Routes
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),

    # Driver Endpoints
    path('drivers/', driver_list, name='driver-list'),
    path('drivers/<int:pk>/', driver_detail, name='driver-detail'),

    # Vehicle Endpoints
    path('vehicles/', vehicle_list, name='vehicle-list'),
    path('vehicles/<int:pk>/', vehicle_detail, name='vehicle-detail'),

    # Location Endpoints
    path('locations/', location_list, name='location-list'),
    path('locations/<int:pk>/', location_detail, name='location-detail'),

    # Trip Endpoints
    path('trips/', trip_list, name='trip-list'),
    path('trip_form_data/', trip_form_data, name='trip-form-data'),
    path('trips/<int:pk>/', trip_detail, name='trip-detail'),

    # Driver Log Endpoints
    path('driver-logs/', driverlog_list, name='driverlog-list'),
    path('driver-logs/<int:pk>/', driverlog_detail, name='driverlog-detail'),

    # Rest Break Endpoints
    path('rest-breaks/', restbreak_list, name='restbreak-list'),
    path('rest-breaks/<int:pk>/', restbreak_detail, name='restbreak-detail'),

    # Fueling Endpoints
    path('fuelings/', fueling_list, name='fueling-list'),
    # path('fuelings/<int:pk>/', fueling_detail, name='fueling-detail'),
]
