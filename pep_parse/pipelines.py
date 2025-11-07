import csv
from datetime import datetime
from collections import defaultdict

from pep_parse import settings

class PepParsePipeline:

    def __init__(self):
        self.results_dir = settings.BASE_DIR / settings.RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.statuses[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        now = datetime.now()
        now_formatted = now.strftime(settings.DATETIME_FORMAT)
        file_name = f'{settings.SUMMARY_NAME}_{now_formatted}.{settings.FILE_FORMAT}'
        file_path = self.results_dir / file_name
        with open(file_path, mode='w', encoding='utf-8') as csvfile:
            csv.writer(
                csvfile,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_NONE,
            ).writerows([
                settings.SUMMARY_TABLE_HEADER,
                *self.statuses.items(),
                (settings.SUMMARY_TABLE_BOTTOM, sum(self.statuses.values())),
            ])