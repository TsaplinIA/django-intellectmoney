# -*- coding: utf-8 -*-
import datetime

from django import forms
from intellectmoney import settings
from intellectmoney.helpers import checkHashOnReceiveResult, getHashOnRequest


class _BaseForm(forms.Form):

    eshopId = forms.CharField(initial=settings.SHOPID)
    orderId = forms.CharField(max_length=50)

    def clean_eshopId(self):
        eshopId = self.cleaned_data['eshopId']
        if eshopId != settings.SHOPID:
            raise forms.ValidationError(u'Неверный eshopId')
        return eshopId


class _BasePaymentForm(_BaseForm):

    CURRENCY_CHOICES = map(lambda x: (x, x), ['RUR', 'TST', 'RUB'])
    serviceName = forms.CharField(label=u'Payment Description', required=False)
    recipientAmount = forms.DecimalField(max_digits=10, decimal_places=2)
    recipientCurrency = forms.ChoiceField(
        choices=CURRENCY_CHOICES, initial=settings.DEBUG and 'TST' or 'RUB'
    )
    userName = forms.CharField(max_length=255, required=False)
    userEmail = forms.EmailField(required=False)


class IntellectMoneyForm(_BasePaymentForm):
    """Payment request form."""

    PREFERENCE_INNER = 'inner'
    PREFERENCE_BANKCARD = 'bankCard'
    PREFERENCE_EXCHANGERS = 'exchangers'
    PREFERENCE_TERMINALS = 'terminals'
    PREFERENCE_TRANSFERS = 'transfers'
    PREFERENCE_SMS = 'sms'
    PREFERENCE_BANK = 'bank'

    # exchangers
    PREFERENCE_TELEMONEY = 'telemoney'
    PREFERENCE_RBKMONEY = 'rbkmoney'
    PREFERENCE_YANDEX = 'yandex'
    PREFERENCE_MONEYMAIL = 'moneymail'
    PREFERENCE_WALET = 'walet'
    PREFERENCE_EASYPAY = 'easypay'
    PREFERENCE_LIQPAY = 'liqpay'
    PREFERENCE_ZPAYMENT = 'zpayment'
    PREFERENCE_QIWIPURSE = 'qiwipurse'
    PREFERENCE_VKONTAKTEBANK = 'vkontaktebank'
    PREFERENCE_MAILRU = 'mailru'
    PREFERENCE_AMEGAEKO = 'amegaeko'
    PREFERENCE_MOBIMONEY = 'mobimoney'
    PREFERENCE_RAPIDA = 'rapida'
    PREFERENCE_ALFACLICK = 'alfaclick'

    PREFERENCE_CHOICES = [
        # common
        (PREFERENCE_INNER, 'IntellectMoney'),
        (PREFERENCE_BANKCARD, 'Visa/MasterCard'),
        (PREFERENCE_EXCHANGERS, u'Internet Exchangers'),
        (PREFERENCE_TERMINALS, u'Terminals'),
        (PREFERENCE_TRANSFERS, u'Transfers'),
        (PREFERENCE_SMS, 'SMS'),
        (PREFERENCE_BANK, u'Bank'),
        # exchangers
        (PREFERENCE_TELEMONEY, 'Telemoney'),
        (PREFERENCE_RBKMONEY, 'RBKMoney'),
        (PREFERENCE_YANDEX, u'Яндекс.деньги'),
        (PREFERENCE_MONEYMAIL, u'MoneyMail'),
        (PREFERENCE_WALET, u'Единый кошелек'),
        (PREFERENCE_EASYPAY, u'EasyPay'),
        (PREFERENCE_LIQPAY, u'LiqPay'),
        (PREFERENCE_ZPAYMENT, u'Zpayment'),
        (PREFERENCE_QIWIPURSE, u'QIWI Кошелек'),
        (PREFERENCE_VKONTAKTEBANK, u'В Контакте'),
        (PREFERENCE_MAILRU, u'Деньги@Mail.Ru'),
        (PREFERENCE_AMEGAEKO, u'Единая Кнопка Оплаты'),
        (PREFERENCE_MOBIMONEY, u'С баланса телефона'),
        (PREFERENCE_RAPIDA, u'В салонах связи'),
        (PREFERENCE_ALFACLICK, u'AlfaClick'),
        # groups
        ('inner,bankCard,exchangers,terminals,bank,transfers,sms', u'All'),
        ('bankCard,exchangers,terminals,bank,transfers,sms', u'All without inner'),
    ]

    RECCURING_TYPE_ACTIVATE = 'Activate'
    RECCURING_TYPE_CHOICES = (
        (RECCURING_TYPE_ACTIVATE, RECCURING_TYPE_ACTIVATE),
    )

    successUrl = forms.CharField(
        required=False, max_length=512, initial=settings.SUCCESS_URL
    )
    failUrl = forms.CharField(required=False, max_length=512, initial=settings.FAIL_URL)
    preference = forms.ChoiceField(
        label=u'Payment Method', choices=PREFERENCE_CHOICES, required=False
    )
    expireDate = forms.DateTimeField(required=False)
    holdMode = forms.BooleanField(required=False, initial=settings.HOLD_MODE)
    holdTime = forms.IntegerField(required=False, min_value=0, max_value=119)
    hash = forms.CharField(required=settings.REQUIRE_HASH)
    merchantReceipt = forms.CharField(required=False)
    frame = forms.IntegerField(required=False, min_value=0, max_value=1)
    reccuringType = forms.ChoiceField(required=False, choices=RECCURING_TYPE_CHOICES)
    customerContact = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault('initial', {})
        if settings.REQUIRE_HASH:
            initial['hash'] = getHashOnRequest(initial)
        if settings.HOLD_MODE:
            exp_date = datetime.datetime.now() + settings.EXPIRE_DATE_OFFSET
            initial['expireDate'] = exp_date

        super(IntellectMoneyForm, self).__init__(*args, **kwargs)


class ResultUrlForm(_BasePaymentForm):

    STATUS_CHOICES = [
        (3, u'Создан счет к оплате (СКО) за покупку'),
        (4, u'СКО аннулирован, деньги возвращены пользователю'),
        (7, u'СКО частично оплачен'),
        (5, u'СКО полностью оплачен'),
        (6, u'Cумма заблокирована на СКО, ожидается запрос на списание'),
        (8, u'По СКО был произведен возврат'),
    ]

    RECURRING_STATE_ACTIVATED = 'Activated'
    RECURRING_STATE_DEACTIVATED = 'Deactivated'
    RECURRING_STATE_PAYED = 'Payed'
    RECURRING_STATE_ERROR = 'Error'
    RECURRING_STATE_CHOICES = (
        (RECURRING_STATE_ACTIVATED, RECURRING_STATE_ACTIVATED),
        (RECURRING_STATE_DEACTIVATED, RECURRING_STATE_DEACTIVATED),
        (RECURRING_STATE_PAYED, RECURRING_STATE_PAYED),
        (RECURRING_STATE_ERROR, RECURRING_STATE_ERROR),
    )

    paymentId = forms.CharField(label=u'IntellectMoney Payment ID')
    paymentData = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    paymentStatus = forms.TypedChoiceField(choices=STATUS_CHOICES, coerce=int)
    eshopAccount = forms.CharField()
    hash = forms.CharField()
    secretKey = forms.CharField()
    reccuringState = forms.ChoiceField(choices=RECURRING_STATE_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(ResultUrlForm, self).__init__(*args, **kwargs)
        if settings.SEND_SECRETKEY:
            self.fields['hash'].required = False
            self.fields['secretKey'].required = True
        else:
            self.fields['hash'].required = True
            self.fields['secretKey'].required = False

    def clean_secretKey(self):
        secretKey = self.cleaned_data['secretKey']
        if settings.SEND_SECRETKEY:
            if secretKey != settings.SECRETKEY:
                raise forms.ValidationError(u'Неверное значение')
        return secretKey

    def clean(self):
        data = self.cleaned_data
        if not settings.SEND_SECRETKEY:
            if not checkHashOnReceiveResult(data):
                raise forms.ValidationError(u'Неверный hash')
        return data


class AcceptingForm(_BaseForm):

    ACTION_CHOICES = [('Refund', 'Refund'), ('ToPaid', 'ToPaid')]

    action = forms.ChoiceField(choices=ACTION_CHOICES)
    secretKey = forms.CharField()
