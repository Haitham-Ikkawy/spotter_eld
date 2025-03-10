from ads_platform.models import Operator, ServiceOperator, Service, HostUrl, PageConfig, PageServiceOperator
from helper.redis import cache_tools, redis_tools


def get_service_operator_by_token(auth_token):
    service_op = None

    def _get_obj():
        return ServiceOperator.objects.filter(auth_token=auth_token)

    redis_key = "cache:service_op:%s" % auth_token
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        service_op = cache_result[0]

    return service_op


def get_service_by_id(service_id):
    service_obj = None

    def _get_obj():
        return Service.objects.filter(id=service_id)

    redis_key = "cache:service:id:%s" % service_id
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        service_obj = cache_result[0]

    return service_obj


def get_service_by_slug(service_slug):
    service_obj = None

    def _get_obj():
        return Service.objects.filter(slug=service_slug)

    redis_key = "cache:service:slug:%s" % service_slug
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        service_obj = cache_result[0]

    return service_obj


def get_operator_by_token(auth_token):
    operator_obj = None

    def _get_obj():
        return Operator.objects.filter(auth_token=auth_token)

    redis_key = "cache:operator:%s" % auth_token
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        operator_obj = cache_result[0]

    return operator_obj


def get_operator_by_id(operator_id):
    operator_obj = None

    def _get_obj():
        return Operator.objects.filter(id=operator_id)

    redis_key = "cache:operator:id:%s" % operator_id
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        operator_obj = cache_result[0]

    return operator_obj


def get_operator_by_code(operator_code):
    operator_obj = None

    def _get_obj():
        return Operator.objects.filter(operator_code=operator_code)

    redis_key = "cache:operator:code:%s" % operator_code
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60 * 6)

    if cache_result:
        operator_obj = cache_result[0]

    return operator_obj


def get_host_url_by_url(url):
    host_url_objs = None

    def _get_objs():
        return HostUrl.objects.filter(url=url)

    redis_key = "cache:host_url:%s" % url
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_objs, 60 * 60)

    if cache_result:
        host_url_objs = cache_result[0]

    return host_url_objs


def get_page_configs_by_host_url_and_slug(host_url_obj, slug):
    page_configs_list = None

    def _get_obj():
        return list(PageConfig.objects.select_related('campaign').filter(
            host_url=host_url_obj, slug=slug, is_active=True
        ))

    redis_key = "cache:page_configs:%s:%s" % (host_url_obj.id, slug)
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 15 * 60)

    if cache_result:
        page_configs_list = cache_result

    return page_configs_list


def get_page_config_by_id(page_config_id):
    page_config_obj = None

    def _get_obj():
        return PageConfig.objects.filter(public_id=page_config_id).select_related('host_url')

    redis_key = f"cache:page_config:{page_config_id}"
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60)

    if cache_result:
        page_config_obj = cache_result[0]

    return page_config_obj


def get_page_service_operators_by_page_config_id(page_config_id, operator_code):
    page_service_operators_list = None

    def _get_obj():
        obj = list(PageServiceOperator.objects.select_related('page_config', 'service_operator__service')
                                       .filter(page_config__public_id=page_config_id, service_operator__operator__code=operator_code))


        return obj


    redis_key = f"cache:page_service_operators:{page_config_id}"
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60)
    if cache_result:
        page_service_operators_list = cache_result

    return page_service_operators_list


def get_page_service_operator(page_service_operator_id):
    page_service_operator_obj = None

    def _get_obj():
        return (PageServiceOperator.objects.select_related('page_config', 'service_operator__service')
                .filter(id=page_service_operator_id))

    redis_key = f"cache:page_service_operator:{page_service_operator_id}"
    cache_result = cache_tools.get_model_from_redis(redis_key, _get_obj, 60 * 60)

    if cache_result:
        page_service_operator_obj = cache_result[0]

    return page_service_operator_obj

