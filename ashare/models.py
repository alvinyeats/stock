from django.db import models


# Create your models here.
class AShare(models.Model):
    no = models.CharField('股票代码', max_length=6, unique=True)
    abbr = models.CharField('股票简称', max_length=200)

    def __str__(self):
        return self.no

    class Meta:
        ordering = ['no']
        verbose_name = "A股"
        verbose_name_plural = "A股"


class AShareDaily(models.Model):
    stock = models.ForeignKey(AShare, on_delete=models.CASCADE)
    today = models.DateField('日期')
    price_open = models.FloatField('开盘价')
    price_close = models.FloatField('收盘价')
    price_upper = models.FloatField('最高价', default=0.0)
    price_lower = models.FloatField('最低价', default=0.0)
    rise_rate = models.FloatField('涨跌幅')
    rise_amt = models.FloatField('涨跌额')

    create = models.DateTimeField('创建日期', auto_now_add=True)
    modify = models.DateTimeField('修改日期', auto_now=True)

    def __str__(self):
        return self.stock.no + '@' + self.today.strftime("%Y-%m-%d")

    class Meta:
        unique_together = ("stock", "today")
        ordering = ['-rise_rate']
        verbose_name = "A股每日"
        verbose_name_plural = "A股每日"


