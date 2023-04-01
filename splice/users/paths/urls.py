from django.urls import path
from splice.users.views.create_user import create_user
from splice.users.views.delete_user import delete_user
from splice.users.views.get_transaction_id import get_transaction_id

urlpatterns = [
    path("create-payment-user/", create_user),
    path("delete-payment-user/", delete_user),
    path("get-transaction-id/", get_transaction_id),
]
