from django.contrib import admin
from splice.users.models.user import SpliceUser
from splice.users.models.cards import UsersCard
from splice.payments.models.payments import Payments

# Register your models here.

admin.site.register(SpliceUser)
admin.site.register(UsersCard)
admin.site.register(Payments)
