import csv
from datetime import datetime
from collections import defaultdict

from pep_parse import settings

class PepParsePipeline:
    """Pipeline собирает статистику по статусам и пишет csv-файл со сводкой."""

    def __init__(self):
        self.output_dir = settings.RESULTS_DIR
        self.output_dir.mkdir(exist_ok=True)
        self._status_counts = defaultdict(int)

    def open_spider(self, spider):
        """Вызывается при старте паука, сбрасываем предыдущие данные."""
        self._status_counts.clear()

    def process_item(self, item, spider):
        """Считаем количество каждого статуса PEP."""
        status = item.get("status", "unknown")
        self._status_counts[status] += 1
        return item

    def close_spider(self, spider):
        """По завершении работы паука создаём CSV со сводкой."""
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        summary_file = self.output_dir / f"status_summary_{now_str}.csv"

        total_count = sum(self._status_counts.values())

        with summary_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Статус", "Количество"])
            for status, count in sorted(self._status_counts.items()):
                writer.writerow([status, count])
            writer.writerow(["Total", total_count])