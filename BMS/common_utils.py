# **************** Other Util Methods ****************
import gc
import json
from django.http import HttpResponse
import logging
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger('BMS')

'''
CONSTANTS 
------------------------------------------------------------------------------------------------------------------------
'''

STATUS_OK = True
STATUS_ERROR = False
HTTP_ERROR = 500
HTTP_SUCCESS = 200
RESPONSE_STATUS = "status"
RESPONSE_MESSAGE = "message"
RESPONSE_DATA = "response"
TEXT_OPERATION_UNSUCCESSFUL = "Operation_Unsuccessful"
TEXT_OPERATION_SUCCESSFUL = "Operation_Successful"
# TEXT_SUCCESSFUL = "Operation Successful"
TEXT_SUCCESSFUL = "Record has been added successfully"
TEXT_EDITED_SUCCESSFUL = "Record has been modified successfully"
METHOD_DOES_NOT_EXIST = "The specified method does not exist"
DEFAULT_ERROR_MESSAGE = "There is some issue your request cannot be processed."
TEXT_PARAMS_MISSING = "Params are missing"



ERROR_RESPONSE_BODY = {
    #FOR GENERIC ERRORS THROWN BY EXCEPTION HANDLING DECORATOR
    RESPONSE_STATUS: 500,
    RESPONSE_MESSAGE: DEFAULT_ERROR_MESSAGE,
}

ERROR_PARAMS_MISSING_BODY = {
    RESPONSE_STATUS: HTTP_SUCCESS,
    RESPONSE_MESSAGE: TEXT_PARAMS_MISSING
}

'''
------------------------------------------------------------------------------------------------------------------------
END CONSTANTS
'''
def get_param(request, key, default):
    key = request.query_params.get(key, default)
    return key or default


def get_request_param(request, key, default):
    key = json.loads(request.GET['data'])[key]
    return key or default


def get_data_param(request, key, default):
    if hasattr(request, 'data'):
        key = request.data.get(key, default)
        return key or default
    else:
        return default


def get_data_param_list(request, key, default):
    key = request.get(key)
    return key or default


def get_customer_from_request(request, default):
    customer = request.user.customer.id
    return customer or default


def get_module_from_request(request, default):
    m_id = request.user.preferred_module
    return m_id or default


def get_user_from_request(request, default):
    user = request.user
    return user or default


def get_default_param(request, key, default):
    key = request.query_params.get(key, request.data.get(key, default))
    return key or default


def get_list_param(request, key, default):
    key = request.GET.getlist(key)
    return key or default

#ERROR MESSAGE FOR SERIALIZERS
def error_message_serializers(serializer_errors):
    return serializer_errors[next(iter(serializer_errors))][0]

#DECORATOR FOR EXCEPTIONS
def exception_handler(def_value=None):
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as err:
                logger.error(err, exc_info=True)
                return def_value
        return applicator
    return decorate

#DECORATOR FOR MANDATORY PARAMS IN REQUEST
def verify_request_params(params):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if not all(param in request.query_params for param in params):
                return generic_response(response_body=ERROR_PARAMS_MISSING_BODY, http_status=200)
            return func(request, *args, **kwargs)
        return inner
    return decorator


#ASYNC THREAD INITIALIZER DECORATOR (!!! DO NOT USE UNLESS NECESSARY)
def async_util(f):
    from threading import Thread
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

#NOT USEFUL FOR US
def append_post_request_params(function):
    def wrap(request):
        if request.user.is_authenticated():
            request.POST._mutable = True
            # request.POST['customer'] = get_customer_from_request(request, None)
            request.POST['modified_by'] = get_user_from_request(request, None)
            request.POST['module'] = get_module_from_request(request, None)
            request.POST._mutable = False
        else:
            return function(request)
    return wrap

#USELESS FOR NOW
def verify_user_privileges(params):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.role_id not in params:
                response_body = {RESPONSE_MESSAGE: "You dont have enough privileges", RESPONSE_STATUS: 403}
                return generic_response(response_body=response_body, http_status=200)
            return func(request, *args, **kwargs)
        return inner
    return decorator



# Generic failure/success Response
#USE THIS TO SEND RESPONSE
def generic_response(response_body, http_status=200, header_dict={}, mime='application/json'):
    msg = json.dumps(response_body, cls=DjangoJSONEncoder)
    resp = HttpResponse(msg, status=http_status, content_type=mime)
    for name, value in header_dict.items():
        resp[name] = value
    return resp


def get_value_from_data(key, data, type, default=None):
    if data.get(key):
        if type == 'float':
            return float(data.get(key))
        elif type == 'string':
            return str(data.get(key))
        elif type == 'int':
            return int(data.get(key))
    else:
        return default
