# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from . import models

admin.site.register(models.User, UserAdmin)

# git remote add origin https://github.com/nebeedtp/miniwallet