from django.contrib import admin
from .models import User, Case


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'case_state', 'on_address', 'off_address', 'case_money')