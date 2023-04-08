from django.urls import path
from splice.users.views.create_user import create_user
from splice.users.views.update_user import update_user
from splice.users.views.delete_user import delete_user
from splice.users.views.get_my_cards import get_my_cards
from splice.users.views.authenticate import get_auth_token
from splice.users.views.get_transaction_id import get_transaction_id


urlpatterns = [
    path("create-payment-user/", create_user),
    path("delete-payment-user/", delete_user),
    path("update-payment-user/", update_user),
    path("get-my-cards/", get_my_cards),
    path("get-transaction-id/", get_transaction_id),
    path("get-auth-token/", get_auth_token),
]
