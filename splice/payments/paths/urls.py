from django.urls import path
from splice.payments.views.get_payment_history import get_payment_history
from splice.payments.views.get_sales_history import get_sales_history


urlpatterns = [
    path("get-purchase-history/", get_payment_history),
    path("get-sales-history/", get_sales_history),
]
