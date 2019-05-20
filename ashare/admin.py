from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from .models import AShare, AShareDaily
# Register your models here.


class AShareAdmin(admin.ModelAdmin):
    list_display = ('no', 'abbr', 'industry')
    search_fields = ('no', 'abbr', 'industry')
    list_filter = ('industry', )


class AShareDailyAdmin(admin.ModelAdmin):
    list_display = ('stock', 'today', 'rise_rate', 'rise_amt')
    search_fields = ('stock', 'today', 'rise_rate', 'rise_amt')
    list_filter = (('today', DateRangeFilter), )


admin.site.register(AShare, AShareAdmin)
admin.site.register(AShareDaily, AShareDailyAdmin)
