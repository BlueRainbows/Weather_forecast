from django.contrib import admin
from users.models import User, History

admin.site.register(User)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'data')
