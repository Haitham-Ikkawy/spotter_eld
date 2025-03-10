import logging
import time
from functools import wraps

from django.utils import timezone

from ap_api .dao import web_click_dao
from ap_api .logic import service_operator_logic
from ads_platform import settings
from ads_platform.models import GoogleAdsCampaign
from ads_platform.mongo_models import WebApiTracking, PartnerApiTracking
from helper.common import tools
from helper.common.constants import ResponseMessage, ResponseStatus

log = logging.getLogger(__name__)


def web_page_api_tracking(id_params=None, enable_encryption=False):
    """
    Decorator that log into mongodb collection named 'api_tracking' the requests of the APIs
    @param id_params: list of parameters names in request.GET or request.POST to log them
    @param enable_encryption: Boolean to activate/deactivate encryption/decryption
    """

    def decorator(func):
        @wraps(func)
        def inner_funct(request):
            start_time = time.time()

            # Apply Decoding
            if enable_encryption:
                request = tools.decode_request(request)

            result_dict = func(request)

            function_name = func.__name__
            username = request.user.username if request.user else request.POST.get('username')
            request_params = dict([(param, request.POST.get(param)) for param in id_params if
                                   param in request.POST.keys()]) if id_params else dict()
            request_params.update(dict([(param, request.GET.get(param)) for param in id_params if
                                        param in request.GET.keys()]) if id_params else dict())

            response_status = result_dict.get('status')
            response_message = result_dict.get('message')
            response_dev_message = result_dict.get('dev_message', '')

            response_payload = {}
            if function_name not in ['evina_get_script']:
                response_payload = result_dict.get('payload')

            request_size = request.META.get('CONTENT_LENGTH') if request.META.get('CONTENT_LENGTH') else 0  # size in bytes

            user_agent = request.META.get('HTTP_USER_AGENT')

            request_headers = tools.auth_http_headers_dict(request)

            # Apply Encoding
            if enable_encryption:
                result_dict['payload'] = tools.encode_response(result_dict.get('payload'))

            result = tools.ajax_response(result_dict)

            response_size = len(result.content)  # size in bytes
            execution_time = float("{0:.4f}".format((time.time() - start_time)))

            WebApiTracking.objects.create(
                function_name=function_name,
                created_ts=timezone.now(),
                execution_time=execution_time,
                request_headers=request_headers if request_headers else None,
                request_params=request_params if request_params else None,
                response_status=response_status,
                user_agent=user_agent,
                response_message=response_message if response_message else None,
                response_dev_message=response_dev_message if response_dev_message else None,
                request_size=request_size,
                response_size=response_size,
                ip_address=tools.get_client_ip(request),
                response_payload=response_payload if settings.ENABLE_PAYLOAD_IN_API_TRACKING else None
            )

            log.info(
                "api: %s(username='%s', execution_time='%0.4f second', request_size='%s', response_size='%s', request_method='%s', request_headers='%s') => (status='%s', message='%s')",
                function_name, username, execution_time, request_size, response_size, request.method, request_headers,
                response_status, response_message)

            return result

        return inner_funct

    return decorator


def partner_api_tracking(id_params=None, enable_encryption=False):
    """
    Decorator that log into mongodb collection named 'api_tracking' the requests of the APIs
    @param id_params: list of parameters names in request.GET or request.POST to log them
    @param enable_encryption: Boolean to activate/deactivate encryption/decryption
    """

    def decorator(func):
        @wraps(func)
        def inner_funct(request):
            start_time = time.time()

            # Apply Decoding
            if enable_encryption:
                request = tools.decode_request(request)

            result_dict = func(request)

            function_name = func.__name__
            username = request.user.username if request.user else request.POST.get('username')
            request_params = dict([(param, request.POST.get(param)) for param in id_params if
                                   param in request.POST.keys()]) if id_params else dict()
            request_params.update(dict([(param, request.GET.get(param)) for param in id_params if
                                        param in request.GET.keys()]) if id_params else dict())

            response_status = result_dict.get('status')
            response_message = result_dict.get('message')
            response_dev_message = result_dict.get('dev_message')
            operator_code = result_dict.get('operator_code')
            service_code = result_dict.get('service_code')

            response_payload = {}
            if function_name not in ['evina_get_script']:
                response_payload = result_dict.get('payload')

            request_size = request.META.get('CONTENT_LENGTH') if request.META.get('CONTENT_LENGTH') else 0  # size in bytes

            user_agent = request.META.get('HTTP_USER_AGENT')

            request_headers = tools.auth_http_headers_dict(request)

            # Apply Encoding
            if enable_encryption:
                result_dict['payload'] = tools.encode_response(result_dict.get('payload'))

            result = tools.ajax_response(result_dict)

            response_size = len(result.content)  # size in bytes
            execution_time = float("{0:.4f}".format((time.time() - start_time)))

            PartnerApiTracking.objects.create(
                function_name=function_name,
                created_ts=timezone.now(),
                execution_time=execution_time,
                request_headers=request_headers if request_headers else None,
                request_params=request_params if request_params else None,
                response_status=response_status,
                user_agent=user_agent,
                response_message=response_message if response_message else None,
                response_dev_message=response_dev_message if response_dev_message else None,
                request_size=request_size,
                response_size=response_size,
                ip_address=tools.get_client_ip(request),
                response_payload=response_payload if settings.ENABLE_PAYLOAD_IN_API_TRACKING else None,
                service_code=service_code if service_code else None,
                operator_code=operator_code if operator_code else None
            )

            log.info(
                "api: %s(username='%s', execution_time='%0.4f second', request_size='%s', response_size='%s', request_method='%s', request_headers='%s') => (status='%s', message='%s')",
                function_name, username, execution_time, request_size, response_size, request.method, request_headers,
                response_status, response_message)

            return result

        return inner_funct

    return decorator


def api_return(fn_to_wrap):
    """
    Decorator that returns JSON response. Functions should return dict object
    """

    @wraps(fn_to_wrap)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'device'):
            request.device = None
        if not hasattr(request, 'user'):
            request.user = None
        if not hasattr(request, 'game'):
            request.game = None

        result = {'status': 'FAIL', 'message': 'UNKNOWN_ERROR'}
        try:
            result = fn_to_wrap(request, *args, **kwargs)
        except Exception as x:
            log.error("Failed '%s', user: '%s', device: '%s'", fn_to_wrap.__name__, request.user, request.device,
                      exc_info=True)
            if settings.DEBUG:
                result['dev_message'] = "Failed '%s', %s" % (fn_to_wrap.__name__, str(x))

        return result

    return wrapper


def params_required(GET_LIST=None, POST_LIST=None, HTTP_LIST=None, ignore_default_headers=False):
    """
    Check the if required params sent in the request are all there
    """

    def decorator(func):
        @wraps(func)
        def inner_funct(request, *args, **kwargs):

            if ignore_default_headers:
                final_http_list = []
            else:
                final_http_list = ['HTTP_DEVICE_ID', 'HTTP_DEVICE_TYPE', 'HTTP_APP_VERSION']

            if HTTP_LIST:
                final_http_list.extend(HTTP_LIST)

            missing_params = {
                'GET': tools.missing_params(request.GET, GET_LIST),
                'POST': tools.missing_params(request.POST, POST_LIST),
                'HTTP_HEADERS': tools.missing_params(request.META, final_http_list)
            }

            if missing_params["GET"] or missing_params['POST'] or missing_params['HTTP_HEADERS']:
                returned_object = {key: value for key, value in missing_params.items() if missing_params[key]}
                return {'status': 'FAIL', 'message': 'NOT_ENOUGH_INFO', 'payload': returned_object}

            return func(request, *args, **kwargs)

        return inner_funct

    return decorator


def try_except(fn_to_wrap):
    """
    Decorator that wrapps the function with try, except and log the error with the arguments
    """

    @wraps(fn_to_wrap)
    def wrapper(*args, **kwargs):
        try:
            return fn_to_wrap(*args, **kwargs)
        except:
            log.error("Failed '%s', args: %s", fn_to_wrap.__name__, args, exc_info=True)

    return wrapper


def check_web_page_attributes(object_id_params=None):
    """
    Validate that the specified UUID parameters are present and valid.
    """
    if object_id_params is None:
        object_id_params = []

    def decorator(func):
        @wraps(func)
        def inner_funct(request, *args, **kwargs):
            data = request.POST

            web_click_id = data.get('web_click_id')
            web_click_obj, page_service_operator_obj = None, None

            if tools.is_valid_object_id(web_click_id):
                web_click_obj = web_click_dao.get_web_click(data.get('web_click_id'))

            if web_click_obj:

                request.web_click_obj = web_click_obj

                page_service_operator_obj = service_operator_logic.get_page_service_operator(web_click_obj.page_service_operator_id)

                ga_campaign_obj = None

                if web_click_obj.ga_campaign_id:
                    ga_campaign_obj = GoogleAdsCampaign.objects.filter(ga_campaign_id=web_click_obj.ga_campaign_id).first()

                request.ga_campaign_obj = ga_campaign_obj
                # page_service_operator_obj = redis_dao.get_page_service_operator(web_click_obj.page_service_operator_id)

                if page_service_operator_obj:

                    if page_service_operator_obj.service_operator.is_active:
                        request.page_service_operator_obj = page_service_operator_obj

                    else:
                        log.debug(f"Inactive service operator status for page_service_operator_id={page_service_operator_obj.id}")
                        return {'status': 'FAIL', 'message': ResponseMessage.INACTIVE_SERVICE_OPERATOR}

                else:
                    log.debug(f"No page service operator found for web_click_id: {web_click_id}")
                    request.page_service_operator_obj = page_service_operator_obj
                    # log.error(f"Cannot fetch page_service_operator_obj from web_click_id:  {web_click_id}", exc_info=True)
                    #
                    # return {'status': ResponseStatus.FAIL, 'message': ResponseMessage.PAGE_SERVICE_OPERATOR_NOT_FOUND}
            else:
                log.debug(f"Cannot fetch web_click_id:  {web_click_id}", exc_info=True)

                return {'status': ResponseStatus.FAIL, 'message': ResponseMessage.INVALID_WEB_CLICK_ID}

            return func(request, *args, **kwargs)

        return inner_funct

    return decorator