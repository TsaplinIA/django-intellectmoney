# -*- coding: utf-8 -*-
import hashlib

from intellectmoney import settings


def checkHashOnReceiveResult(data):
    data_hash = getHashOnReceiveResult(data)
    return data_hash == data.get('hash')


def getHashOnReceiveResult(data):
    secretKey = settings.SECRETKEY
    serviceName = data.get('serviceName', '')
    eshopId = data.get('eshopId', '')
    orderId = data.get('orderId', '')
    eshopAccount = data.get('eshopAccount')
    recipientAmount = data.get('recipientAmount', '')
    recipientCurrency = data.get('recipientCurrency', '')
    paymentStatus = data.get('paymentStatus', '')
    userName = data.get('userName', '')
    userEmail = data.get('userEmail', '')
    paymentData = data.get('paymentData')
    paymentData = paymentData.replace(tzinfo=None)
    key = '%s::%s::%s::%s::%.2f::%s::%s::%s::%s::%s::%s' % (
        eshopId,
        orderId,
        serviceName,
        eshopAccount,
        recipientAmount,
        recipientCurrency,
        paymentStatus,
        userName,
        userEmail,
        paymentData,
        secretKey,
    )
    key = key.encode('windows-1251', errors='ignore')
    key_hash = hashlib.md5(key).hexdigest()
    return key_hash


def getHashOnRequest(data):
    secretKey = settings.SECRETKEY
    serviceName = data.get('serviceName', '')
    eshopId = data.get('eshopId')
    orderId = data.get('orderId')
    recipientAmount = data.get('recipientAmount')
    recipientCurrency = data.get('recipientCurrency')
    recurringType = data.get('recurringType')
    if recurringType:
        key = '%s::%s::%s::%s::%s::%s::%s' % (
            eshopId,
            orderId,
            serviceName,
            recipientAmount,
            recipientCurrency,
            recurringType,
            secretKey,
        )
    else:
        key = '%s::%s::%s::%s::%s::%s' % (
            eshopId,
            orderId,
            serviceName,
            recipientAmount,
            recipientCurrency,
            secretKey,
        )
    key = key.encode('windows-1251', errors='ignore')
    key_hash = hashlib.md5(key).hexdigest()
    return key_hash
