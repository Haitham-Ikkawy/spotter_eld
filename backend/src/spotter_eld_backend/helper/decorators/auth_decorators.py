import json
import logging
import pickle
import time
from functools import wraps

from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from ads_platform import settings
from helper.redis import redis_dao
from helper.common.constants import ResponseMessage
# from num_play.logic.account_logic import check_for_mandatory_updates
# from ads_platform.models import Device, OperatorAffiliate, CountryAffiliate, Affiliate, Operator
from ads_platform.models import Operator
# from helper.decorators.api_decorators import check_maintenance
from helper.common import tools

log = logging.getLogger(__name__)


# def api_auth(func):
#     """
#     Decorator for User/Device authentication, it checks the request headers for the device, and embed the user and device objects in the request
#     """
#
#     @wraps(func)
#     @check_maintenance
#     def closure(request, *args, **kwargs):
#
#         auth_token, device_id, app_version, device_type = tools.auth_http_headers(request, possible_headers=['auth_token', 'device_id', 'app_version', 'device_type'])
#         # log.debug("auth_token %s, device_id %s, app_version %s, device_type %s", auth_token, device_id, app_version, device_type)
#         try:
#             # user, device = None, None
#             # if auth_token and auth_token != 'null':
#             user, device = redis_dao.get_user_device_by_auth_token(device_type, auth_token)
#
#             if user and device:
#                 if device.device_id != device_id:  # and device_id != 'null':
#                     # log.debug("1- auth_token %s, device_id %s, app_version %s, device_type %s", auth_token, device_id, app_version, device_type)
#
#                     return tools.ajax_response(tools.create_response(message=ResponseMessage.INVALID_AUTH_TOKEN))
#             else:
#                 if auth_token:  # and auth_token != 'null' and device_id and device_id != 'null':
#                     # not found in redis then get from DB
#                     qset = Q(auth_token=auth_token, device_type=device_type, is_loggedin=True, device_id=device_id)
#                     device = Device.objects.select_related('user').filter(qset).first()
#
#                     if device and device.user:
#                         redis_dao.set_user_device_by_auth_token(device.user, device)
#                         user = device.user
#
#                     else:
#                         # log.debug("2- auth_token %s, device_id %s, app_version %s, device_type %s", auth_token, device_id, app_version, device_type)
#
#                         return tools.ajax_response(tools.create_response(message=ResponseMessage.INVALID_AUTH_TOKEN))
#                 else:
#                     if device_type.upper() != DeviceType.WEB or func.__name__ not in ['search_card_web', 'get_card_by_username', 'get_download_card_vcf', 'submit_verify_email', 'get_store_url',
#                                                                                       'contact_us', 'unsubscribe_email', 'user_onboarding']:
#                         # log.debug("3- auth_token %s, device_id %s, app_version %s, device_type %s, func.__name__: %s", auth_token, device_id, app_version, device_type, func.__name__)
#
#                         return tools.ajax_response(tools.create_response(message=ResponseMessage.INVALID_AUTH_TOKEN))
#
#             # if device_type != DeviceType.WEB and check_for_mandatory_updates(device_type, app_version):
#             #     return tools.ajax_response(tools.create_response(message=ResponseMessage.MANDATORY_UPDATE))
#
#             request.user = user
#             if user:
#                 request.user.device = device
#             request.device = device
#
#         except:
#             log.error("Error in api_auth for function: '%s' decorator for auth_token: '%s', device_id: '%s', app_version: '%s', device_type: '%s'",
#                       func.__name__, auth_token, device_id, app_version, device_type, exc_info=1)
#             return tools.ajax_response(tools.create_response(message=ResponseMessage.UNKNOWN_ERROR))
#
#         return func(request, *args, **kwargs)
#
#     return closure


def permissions_required(perms, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):

        # First check if the user has the permission (even anon users)
        if any([user.has_perms((perm,)) for perm in perms]):
            return True

        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied

        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)


# def affiliate_auth(func):
#     """
#     Decorator for  authentication for OperatorAffiliate
#     """
#
#     @wraps(func)
#     def closure(request, *args, **kwargs):
#         auth_token = kwargs.get('auth_token')
#         try:
#             if auth_token:
#                 # try to get country auth first
#                 country_affiliate = CountryAffiliate.objects.select_related('affiliate').filter(auth_token=auth_token).first()
#                 if country_affiliate:
#                     qset = Q(country_affiliate=country_affiliate)
#                 else:
#                     qset = Q(auth_token=auth_token)
#
#                 operator_affiliate = OperatorAffiliate.objects.select_related('affiliate').filter(qset).first()
#                 if operator_affiliate:
#
#                     request.affiliate = operator_affiliate.affiliate
#                     request.operator = operator_affiliate.operator
#                     request.operator_affiliate = operator_affiliate
#
#                 else:
#                     return tools.create_response(message=ResponseMessage.OPERATOR_AFFILIATE_NOT_RECOGNIZED)
#             else:
#                 return tools.create_response(message=ResponseMessage.MISSING_CREDENTIALS)
#         except:
#             log.error("Error in identify_affiliate for function: '%s' decorator for authorization: '%s'",
#                       func.__name__, auth_token, exc_info=True)
#             return tools.create_response(message=ResponseMessage.UNKNOWN_ERROR)
#
#         return func(request, *args, **kwargs)
#
#     return closure


def service_auth(func):
    """
    Decorator to authenticate service (hundred seconds, ...)
    """

    @wraps(func)
    def closure(request, *args, **kwargs):
        service_code = kwargs.get('service_code')
        ip_address = tools.get_client_ip(request)
        try:
            if service_code in ['HUNDRED_SECONDS'] and ip_address in ['123.123.123.123']:
                # this service is allowed to use Numplay apis
                request.service_code = service_code

            else:
                return tools.create_response(message=ResponseMessage.UNAUTHORIZED_SERVICE)

        except:
            log.error("Service: '%s' from ip address: '%s' is  not authorized", service_code, ip_address, exc_info=True)
            return tools.create_response(message=ResponseMessage.UNKNOWN_ERROR)

        return func(request, *args, **kwargs)

    return closure



# def influencer_auth(func):
#     """
#     Decorator for  authentication for OperatorAffiliate or influencer from public id
#     """
#
#     @wraps(func)
#     def closure(request, *args, **kwargs):
#         slug = kwargs.get('aff_slug')
#         operator_code = request.POST.get('operator_code')
#
#         try:
#             if slug:
#                 # try to get country auth influencer first
#                 influencer_obj = Affiliate.objects.filter(slug=slug, is_influencer=True).first()
#                 if influencer_obj:
#                     request.affiliate = influencer_obj
#                     request.operator = None
#                     request.operator_affiliate = None
#                 else:
#                     operator = Operator.objects.filter(code=operator_code).first()
#                     operator_affiliate = OperatorAffiliate.objects.select_related('affiliate').filter(operator=operator, affiliate__slug=slug).first()
#                     if operator_affiliate:
#
#                         request.affiliate = operator_affiliate.affiliate
#                         request.operator = operator_affiliate.operator
#                         request.operator_affiliate = operator_affiliate
#
#                     else:
#                         return tools.create_response(message=ResponseMessage.OPERATOR_AFFILIATE_NOT_RECOGNIZED)
#             else:
#                 return tools.create_response(message=ResponseMessage.MISSING_CREDENTIALS)
#         except:
#             log.error("Error in identify_affiliate for function: '%s' decorator for authorization: '%s'",
#                       func.__name__, slug, exc_info=True)
#             return tools.create_response(message=ResponseMessage.UNKNOWN_ERROR)
#
#         return func(request, *args, **kwargs)
#
#     return closure
