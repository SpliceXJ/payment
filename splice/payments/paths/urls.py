from django.urls import path
from splice.payments.views.get_payment_history import get_payment_history
from splice.payments.views.get_sales_history import get_sales_history
from splice.payments.views.create_payment_instance import create_payment_instance
from splice.payments.views.verify_payment import verify_payment
from splice.payments.views.pay_using_my_card import pay_with_saved_card


urlpatterns = [
    path("get-purchase-history/", get_payment_history),
    path("get-sales-history/", get_sales_history),
    path("create-payment-instance/", create_payment_instance),
    path("verify-payment/", verify_payment),
    path("pay-using-saved-card/", pay_with_saved_card),
]
