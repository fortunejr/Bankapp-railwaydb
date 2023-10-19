from django.contrib import admin
from .models import Account, DebitHistory, CreditHistory

admin.site.register(Account)
admin.site.register(DebitHistory)
admin.site.register(CreditHistory)