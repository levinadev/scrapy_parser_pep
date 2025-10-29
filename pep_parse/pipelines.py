# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from collections import Counter
import datetime as dt
from pathlib import Path
from scrapy.exceptions import DropItem


class PepParsePipeline:
    def __init__(self):
        # Словарь для хранения счетчика статусов
        self.stats_counter = Counter()

    def open_spider(self, spider):
        # Определяем директорию results
        self.results_dir = Path(spider.settings.get('BASE_DIR', Path(__file__).parent.parent)) / 'results'
        self.results_dir.mkdir(exist_ok=True)
        self.now = dt.datetime.now()

    def process_item(self, item, spider):
        # Считаем количество документов для каждого статуса
        if item.get('status'):
            self.stats_counter[item['status']] += 1
        else:
            # Отбрасываем элемент, если нет статуса (хотя по заданию все должны быть)
            raise DropItem(f"Не найден статус для PEP: {item['number']}")
        return item

    def close_spider(self, spider):
        # Вызывается, когда паук завершил работу

        # Общее количество документов
        total = sum(self.stats_counter.values())

        # Формирование данных для второго CSV-файла (сводка)
        data = [
            ('Статус', 'Количество'),  # Заголовок
        ]

        # Строки со статусами и количеством
        for status, count in self.stats_counter.items():
            data.append((status, str(count)))

        # Последняя строка с общим количеством
        data.append(('Total', str(total)))

        # Формирование имени файла
        # Маска: status_summary_2029-01-31_23-55-00.csv
        datetime_format = '%Y-%m-%d_%H-%M-%S'
        filename = self.now.strftime(f'status_summary_{datetime_format}.csv')
        file_path = self.results_dir / filename

        # Запись данных в CSV-файл
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        spider.logger.info(f'Файл со сводкой по статусам сохранен: {file_path}')
