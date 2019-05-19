from django.contrib import admin

from .models import AShare, AShareDaily
# Register your models here.


class AShareAdmin(admin.ModelAdmin):
    list_display = ('no', 'abbr')
    search_fields = ('no', 'abbr')


class AShareDailyAdmin(admin.ModelAdmin):
    list_display = ('stock', 'today', 'rise_rate', 'rise_amt')
    search_fields = ('stock', 'today', 'rise_rate', 'rise_amt')


admin.site.register(AShare, AShareAdmin)
admin.site.register(AShareDaily, AShareDailyAdmin)
