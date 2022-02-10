from django.contrib import admin
from .models import AppData , CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(AppData)

class CustomUserAdmin(UserAdmin):
        list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff','is_superuser','birthday','phone','gender')
        search_fields = ('email', 'username',)
        readonly_fields = ('date_joined', 'last_login')
        ordering = ('email',)
        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)


