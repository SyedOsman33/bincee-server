from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import BinceeAssets
from BMS.common_utils import generic_response, exception_handler, ERROR_RESPONSE_BODY, HTTP_ERROR_CODE, RESPONSE_DATA, \
    RESPONSE_STATUS, TEXT_PARAMS_MISSING, RESPONSE_MESSAGE, HTTP_SUCCESS_CODE, get_user_from_request, get_data_param, \
    error_message_serializers, TEXT_OPERATION_SUCCESSFUL, get_default_param
from BinceeAssets.models import BinceeEntities
from BinceeAssets.serializers import BinceeAssetsSerializer
from BinceeAssets.utils import get_all_assets_of_type
from user.enums import RoleTypeEnum


@api_view(['POST'])
@permission_classes((AllowAny,))
@exception_handler(generic_response(response_body=ERROR_RESPONSE_BODY, http_status=HTTP_ERROR_CODE))
def add_assets(request):
    '''
    :param request:
    :return: Add asset of given type.
    '''
    response_body = {RESPONSE_MESSAGE: TEXT_PARAMS_MISSING, RESPONSE_STATUS: HTTP_ERROR_CODE, RESPONSE_DATA: []}
    http_status = HTTP_SUCCESS_CODE
    user = get_user_from_request(request, None)
    type_id = int(get_data_param(request, 'type', 0))


    if user.role.id != RoleTypeEnum.ADMIN:
        http_status = HTTP_SUCCESS_CODE
        response_body[RESPONSE_MESSAGE] = 'You do not have sufficient privileges to perform this action.'
        response_body[RESPONSE_STATUS] = HTTP_ERROR_CODE
        return generic_response(response_body=response_body, http_status=http_status)

    if type_id:
        serializer = BinceeAssetsSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            entity = serializer.save()

            http_status = HTTP_SUCCESS_CODE
            response_body[RESPONSE_MESSAGE] = TEXT_OPERATION_SUCCESSFUL
            response_body[RESPONSE_STATUS] = HTTP_SUCCESS_CODE
            response_body[RESPONSE_DATA] = serializer.data
            return generic_response(response_body=response_body, http_status=http_status)

        else:
            for errors in serializer.errors:
                if errors == 'non_field_errors':
                    response_body[RESPONSE_MESSAGE] = serializer.errors[errors][0]
                else:
                    response_body[RESPONSE_MESSAGE] = error_message_serializers(serializer.errors)
            response_body[RESPONSE_STATUS] = HTTP_ERROR_CODE
            return generic_response(response_body=response_body, http_status=http_status)


@api_view(['PATCH', 'POST'])
@exception_handler(generic_response(response_body=ERROR_RESPONSE_BODY, http_status=HTTP_ERROR_CODE))
def edit_assets(request):
    '''
    :param request:
    :return: edit the details of given assets ID and data modified.
    '''
    response_body = {RESPONSE_MESSAGE: TEXT_PARAMS_MISSING, RESPONSE_STATUS: HTTP_ERROR_CODE, RESPONSE_DATA: []}
    http_status = HTTP_SUCCESS_CODE
    user = get_user_from_request(request, None)
    type_id = int(get_data_param(request, 'type', 0))
    p_key = int(get_data_param(request, 'pk', 0))


    if user.role.id == RoleTypeEnum.ADMIN or RoleTypeEnum.MANAGER:
        http_status = HTTP_SUCCESS_CODE
        response_body[RESPONSE_MESSAGE] = 'You do not have sufficient privileges to perform this action.'
        response_body[RESPONSE_STATUS] = HTTP_ERROR_CODE
        return generic_response(response_body=response_body, http_status=http_status)
    try:
        asset = BinceeEntities.objects.get(pk=p_key)
    except:
        asset = None

    if type_id:
        serializer = BinceeAssetsSerializer(asset, data=request.data, context={'request': request})

        if serializer.is_valid():
            entity = serializer.save()

            http_status = HTTP_SUCCESS_CODE
            response_body[RESPONSE_MESSAGE] = TEXT_OPERATION_SUCCESSFUL
            response_body[RESPONSE_STATUS] = HTTP_SUCCESS_CODE
            response_body[RESPONSE_DATA] = serializer.data
            return generic_response(response_body=response_body, http_status=http_status)

        else:
            for errors in serializer.errors:
                if errors == 'non_field_errors':
                    response_body[RESPONSE_MESSAGE] = serializer.errors[errors][0]
                else:
                    response_body[RESPONSE_MESSAGE] = error_message_serializers(serializer.errors)
            response_body[RESPONSE_STATUS] = HTTP_ERROR_CODE
            return generic_response(response_body=response_body, http_status=http_status)


@csrf_exempt
@api_view(['GET'])
@exception_handler(generic_response(response_body=ERROR_RESPONSE_BODY, http_status=HTTP_ERROR_CODE))
def get_assets_list(request):
    '''
    :param request:
    :return: list of all assets of given type. list of JSONs
    '''
    response_body = {RESPONSE_MESSAGE: "", RESPONSE_STATUS: HTTP_SUCCESS_CODE, RESPONSE_DATA: []}
    # c_id = get_customer_from_request(request, None)
    type_id = get_default_param(request, 'type_id', None)

    if type_id:
        response_body[RESPONSE_DATA] = get_all_assets_of_type(type_id=int(type_id), context={'request': request})
        response_body[RESPONSE_STATUS] = HTTP_SUCCESS_CODE
        response_body[RESPONSE_MESSAGE] = TEXT_OPERATION_SUCCESSFUL
    else:
        response_body[RESPONSE_STATUS] = HTTP_ERROR_CODE
        response_body[RESPONSE_MESSAGE] = TEXT_PARAMS_MISSING
        response_body[RESPONSE_DATA] = [{}]
    return generic_response(response_body=response_body, http_status=200)


