from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.User)
class CustomerAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "customer_xid")