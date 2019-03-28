# coding: utf-8
import decimal
import json
import logging
import socket
from enum import IntEnum
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from intellectmoney import settings

CONTENT_TYPE_RECEIPT = 1
CONTENT_TYPE_RETURN_RECEIPT = 2
CONTENT_TYPE_EXPENSES = 3
CONTENT_TYPE_RETURN_EXPENSES = 4


TAX_NDS_20 = 1  # ставка НДС 20%
TAX_NDS_10 = 2  # ставка НДС 10%
TAX_NDS_20_120 = 3  # ставка НДС расч. 20/120
TAX_NDS_10_110 = 4  # ставка НДС расч. 10/110
TAX_NDS_0 = 5  # ставка НДС 0%
TAX_NO_NDS = 6  # НДС не облагается


def getMerchantReceiptPosition(quantity, price, tax, text):
    return {'quantity': quantity, 'price': price, 'tax': tax, 'text': text}


def getMerchantReceiptString(
    inn,
    customer_contact,
    positions,
    group='Main',
    content_type=CONTENT_TYPE_RECEIPT,
    skipAmountCheck=False,
):
    data = {
        'inn': inn,
        'group': group,
        'skipAmountCheck': int(skipAmountCheck),
        'content': {
            'type': content_type,
            'customerContact': customer_contact,
            'positions': positions,
        },
    }
    return json.dumps(data, ensure_ascii=False)


def _make_api_request(url, data, timeout=None):
    data = urlencode(data).encode('utf-8')
    request = Request(
        url=url,
        method='POST',
        data=data,
        headers={'Accept': 'application/json'},
    )
    try:
        result = urlopen(request, timeout=timeout)
    except URLError as exc:
        logging.info('url error: %s', exc)
        raise exc
    except socket.timeout as exc:
        logging.info('timeout: %s', exc)
        raise exc

    result = result.read()

    try:
        result = json.loads(result, parse_float=decimal.Decimal)
    except json.JSONDecodeError as exc:
        logging.info('invalid json from intellectmoney')
        raise exc
    return result


def _parse_response(data):
    operation_state = data.get('OperationState').get('Code')
    if operation_state != ServiceOperationState.SUCCESS:
        raise Exception

    result = data.get('Result')
    return result


class ServiceOperationState(IntEnum):
    SUCCESS = 0
    RUNNING = 1
    ERROR = 2


class RequestState(IntEnum):
    SUCCESS = 0
    SUCCESS_WITH_WARNIGNS = 1
    AUTH_FAIL = 2


def getUserToken():
    if settings.LOGIN is None or settings.PASSWORD is None:
        raise RuntimeError('To use IntellectMoney API you must specify Login and Password')

    data = (('Login', settings.LOGIN), ('Password', settings.PASSWORD))
    result = _make_api_request(settings.GET_USER_TOKEN_URL, data)
    result = _parse_response(result)

    if not result.get('State').get('Code') == RequestState.SUCCESS:
        raise Exception

    token = result.get('UserToken')

    return token


def setScheduledOperation(user_token, payment_id, amount, repeat_plan, params=None):
    data = {
        'UserToken': user_token,
        'ObjectId': payment_id,
        'ObjectTypeVal': 1,
        'ParamsJson': {'Amount': amount},
        'RepeatPlan': repeat_plan,
        'FireOnSkip': 1,
        'State': 1,
        'EndExecDate': '1.1.2099',
        'RetryOnFailPlan': "0 0/15 * 1/1 * ? *",
        'RetryOnFailCount': 3,
        'IsSingle': 0,
    }

    if params:
        data.update(params)

    result = _make_api_request(settings.SET_SHEDULED_OPERATION_URL, data)
    result = _parse_response(result)
    return result


def editScheduledOperation(user_token, operation_id, data):
    data['OperationId'] = operation_id
    result = _make_api_request(settings.SET_SHEDULED_OPERATION_URL, data)
    result = _parse_response(result)
    return result


def getScheduledOperation(user_token, skip=0, take=10):
    data = {
        'UserToken': user_token,
        'Skip': skip,
        'Take': take,
    }
    result = _make_api_request(settings.GET_SHEDULED_OPERATION_URL, data)
    result = _parse_response(result)
    return result
