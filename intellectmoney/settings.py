# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import lazy

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

URL = getattr(settings, 'INTELLECTMONEY_URL', 'https://merchant.intellectmoney.ru/ru/')
GET_USER_TOKEN_URL = 'https://api.intellectmoney.ru/personal/user/getUserToken'
GET_INVOICES_HISTORY_URL = (
    'https://api.intellectmoney.ru/personal/payment/getInvoicesHistory'
)
GET_PAYMENTS_HISTORY_URL = (
    'https://api.intellectmoney.ru/personal/payment/getPaymentsHistory'
)
SET_SHEDULED_OPERATION_URL = (
    'https://api.intellectmoney.ru/personal/scheduler/setScheduledOperationData'
)
GET_SHEDULED_OPERATION_URL = (
    'https://api.intellectmoney.ru/personal/scheduler/getScheduledOperationData'
)
LOGIN = getattr(settings, 'INTELLECTMONEY_LOGIN', None)
PASSWORD = getattr(settings, 'INTELLECTMONEY_PASSWORD', None)

CHECK_IP_ENABLED = getattr(settings, 'INTELLECTMONEY_CHECK_IP_ENABLED', True)
IP = getattr(settings, 'INTELLECTMONEY_IP', '91.212.151.242')

SHOPID = getattr(settings, 'INTELLECTMONEY_SHOPID', None)
SECRETKEY = getattr(settings, 'INTELLECTMONEY_SECRETKEY', None)

DEBUG = getattr(settings, 'INTELLECTMONEY_DEBUG', True)
UNIQUE_ID = getattr(settings, 'INTELLECTMONEY_UNIQUE_ID', False)
REQUIRE_HASH = getattr(settings, 'INTELLECTMONEY_REQUIRE_HASH', False)
SEND_SECRETKEY = getattr(settings, 'INTELLECTMONEY_SEND_SECRETKEY', False)
HOLD_MODE = getattr(settings, 'INTELLECTMONEY_HOLD_MODE', False)
EXPIRE_DATE_OFFSET = getattr(
    settings, 'INTELLECTMONEY_EXPIRE_DATE_OFFSET', datetime.timedelta(days=7)
)
MAIL_FAIL_SILENTLY = getattr(settings, 'INTELLECTMONEY_MAIL_FAIL_SILENTLY', True)


def get_url(name):
    return 'http://%s%s' % (get_current_site(request=None), reverse(name))


SUCCESS_URL = getattr(
    settings,
    'INTELLECTMONEY_SUCCESS_URL',
    lazy(lambda: get_url('intellectmoney-success'), str),
)
FAIL_URL = getattr(
    settings,
    'INTELLECTMONEY_FAIL_URL',
    lazy(lambda: get_url('intellectmoney-fail'), str),
)
