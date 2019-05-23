from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from admin_totals.admin import ModelAdminTotals
import csv
from openpyxl import Workbook

from django.http import FileResponse

from .models import AShare, AShareDaily


# Register your models here.


@admin.register(AShare)
class AShareAdmin(admin.ModelAdmin):
    list_display = ('no', 'abbr', 'industry')
    search_fields = ('no', 'abbr', 'industry')
    list_filter = ('industry', )


def download_total(modeladmin, request, queryset):
    file_path = 'results.xlsx'
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(['行业', '股票代码', '名称', '涨跌幅度'])
    industrys = list(set(queryset.values_list("stock__industry", flat=True)))
    top = dict()
    for industry in industrys:
        cache = dict()
        top[industry] = []
        stocks = list(set(queryset.filter(stock__industry=industry).values_list("stock__no", flat=True)))
        for no in stocks:
            s_sets = queryset.filter(stock__no=no)
            cache[no] = sum([i.rise_rate for i in s_sets])
        cache_sorted = [(k, cache[k]) for k in sorted(cache, key=cache.get, reverse=True)]
        top[industry] = cache_sorted[:5]

    for industry, tops in top.items():
        for top in tops:
            stock = AShare.objects.get(no=top[0])
            ws.append([industry, stock.no, stock.abbr, top[1]])
    wb.save(file_path)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="results.xlsx"'
    response["status"] = 200
    return response


download_total.short_description = "下载统计数据"


@admin.register(AShareDaily)
class AShareDailyAdmin(admin.ModelAdmin):
    list_display = ('stock', 'today', 'rise_rate', 'rise_amt')
    search_fields = ('stock', 'today', 'rise_rate', 'rise_amt')
    list_filter = (('today', DateRangeFilter), 'stock__industry')
    actions = [download_total]



