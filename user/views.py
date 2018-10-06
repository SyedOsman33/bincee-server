from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user.serializers import UserLoginSerializer

__author__ = 'SyedUsman'
__version__ = '1.0'


from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token

# Create your views here.
from BMS.common_utils import get_data_param, exception_handler, generic_response, ERROR_RESPONSE_BODY, HTTP_ERROR_CODE, \
    RESPONSE_MESSAGE, TEXT_PARAMS_MISSING, RESPONSE_STATUS, RESPONSE_DATA, HTTP_SUCCESS_CODE, TEXT_OPERATION_SUCCESSFUL, \
    TEXT_PARAMS_INCORRECT


@api_view(['POST'])
@permission_classes((AllowAny,))
@exception_handler(generic_response(response_body=ERROR_RESPONSE_BODY, http_status=HTTP_ERROR_CODE))
def user_login(request):
    response_body = {RESPONSE_MESSAGE: TEXT_PARAMS_MISSING, RESPONSE_STATUS: HTTP_ERROR_CODE, RESPONSE_DATA: []}
    http_status = HTTP_SUCCESS_CODE


    email = get_data_param(request, 'email', None)
    password = get_data_param(request, 'password', None)
    # push_key = get_data_param(request, 'push_key', None)
    if email and password:
        user = authenticate(username=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)
            user_serializer = UserLoginSerializer(user, context={'request': request})
            # user_modules = ModuleAssignment.objects.filter(customer=user.customer)
            # customer_serializer = CustomerListSerializer(user.customer)
            data = user_serializer.data
            # data['customer'] = customer_serializer.data
            data['token'] = token[0].key
            data['user_role_id'] = None if not user.role else user.role.id
            data['user_role_name'] = None if not user.role else user.role.name
            data['avatar'] = None if not user.avatar else request.build_absolute_uri(user.avatar.url)
            user.save()

            response_body[RESPONSE_MESSAGE] = TEXT_OPERATION_SUCCESSFUL
            response_body[RESPONSE_STATUS] = HTTP_SUCCESS_CODE
            response_body[RESPONSE_DATA] = data

            return generic_response(response_body=response_body, http_status=http_status)

        response_body[RESPONSE_MESSAGE] = TEXT_PARAMS_INCORRECT
        return generic_response(response_body=response_body, http_status=http_status)
    return generic_response(response_body=response_body, http_status=http_status)
