from django.contrib import admin
from app.models import CustomUser, Invite, ChatLabel, ChatRecord

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_login', 'chatrecord_count')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'date_joined', 'last_login')}),

    )

    def chatrecord_count(self, obj):
        return obj.chat_records.count()

    chatrecord_count.short_description = '聊天数目'


class InviteAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'claimed_by')
    search_fields = ('code', 'user__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'claimed_by')
    fieldsets = (
        (None, {
            'fields': ('code', 'user')
        }),
        ('统计信息', {
            'fields': ('created_at', 'claimed_by')
        }),
    )



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Invite, InviteAdmin)
