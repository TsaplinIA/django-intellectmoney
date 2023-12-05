#coding: utf-8
from django.dispatch import Signal

# providing_args:
#     "orderId",
#     "recipientAmount",
#     "reccuringState",
#     "paymentId",
result_received = Signal()
