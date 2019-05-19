from django.core.management.base import BaseCommand
from django.utils import timezone

from ashare.utils import spider_main


class Command(BaseCommand):
    help = 'crawl stock base info'

    def add_arguments(self, parser):
        # total 179
        parser.add_argument('-p', type=int, help='total page')

    def handle(self, *args, **kwargs):
        pages = kwargs['p']
        spider_main(pages)