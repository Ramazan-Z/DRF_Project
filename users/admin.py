from django.contrib import admin

from users.models import Pyment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("email", "username")
    list_filter = ("sity",)
    search_fields = ("username",)


@admin.register(Pyment)
class PymentAdmin(admin.ModelAdmin):

    list_display = ("user", "created_at", "amount")
    list_filter = ("pyment_method",)
    search_fields = ("course", "lesson")
