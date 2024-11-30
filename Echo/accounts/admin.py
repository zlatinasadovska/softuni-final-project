from django.contrib import admin
from Echo.accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_artist')
    list_filter = ('is_staff', 'is_active', 'is_artist')
    search_fields = ('email', 'username')
    ordering = ('email',)

