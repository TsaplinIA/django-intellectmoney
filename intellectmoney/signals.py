#coding: utf-8
from django.dispatch import Signal

result_received = Signal(providing_args=[
    "orderId",
    "recipientAmount",
    "reccuringState",
    "paymentId"
])
