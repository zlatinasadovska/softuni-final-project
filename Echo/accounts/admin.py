from django.contrib import admin
from Echo.accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            restricted_fields = ['is_superuser', 'groups', 'user_permissions']
            return [field for field in fields if field not in restricted_fields]
        return fields


admin.site.site_header = "Echo Admin Panel"
admin.site.site_title = "Echo Admin"
admin.site.index_title = "Welcome to Echo Administration"
