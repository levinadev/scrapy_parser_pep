"""
pep_parse/pipelines.py

Pipeline для Scrapy-паука `PepSpider`, который:
1. Собирает статистику по статусам PEP-документов.
2. Формирует CSV-отчёт с количеством документов по каждому статусу.
3. Логирует процесс обработки и возможные ошибки.

Файл CSV создаётся в директории `settings.RESULTS_DIR` и имеет формат:
'status_summary_YYYY-MM-DD_HH-MM-SS.csv'

Структура CSV:
    - Статус: название статуса PEP
    - Количество: число документов с данным статусом
    - Последняя строка Total: суммарное количество документов
"""
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import logging
from typing import DefaultDict

import scrapy

from pep_parse import settings


class PepParsePipeline:
    """
    Pipeline собирает статистику по статусам PEP-документов
    и записывает сводный отчёт в CSV-файл.

    После завершения работы паука создаётся файл формата:
    'status_summary_YYYY-MM-DD_HH-MM-SS.csv'

    В файле содержатся два столбца:
        - 'Статус': название статуса PEP;
        - 'Количество': число документов с данным статусом;
    Строка файла 'Total' содержит суммарное количество документов.
    """

    def __init__(self) -> None:
        """
        Инициализирует директорию для вывода результатов
        и создаёт внутренний словарь для подсчёта статусов.

        params:
            None
        return:
            None
        """
        # Папка для сохранения CSV-файлов с результатами
        self.output_dir: Path = settings.RESULTS_DIR
        # Создаём директорию, если её нет
        self.output_dir.mkdir(exist_ok=True)
        # Словарь для подсчёта количества документов по каждому статусу
        self._status_counts: DefaultDict[str, int] = defaultdict(int)
        # Логгер
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider: scrapy.Spider) -> None:
        """
        Вызывается при запуске паука.
        Очищает накопленные ранее данные по статусам.

        params:
            spider (scrapy.Spider): Экземпляр текущего паука,
                запускающего процесс парсинга.
        return:
            None
        """
        self._status_counts.clear()
        self.logger.info(
            f'[{spider.name}] Pipeline запущен. '
            f'Счётчики статусов сброшены.'
        )

    def process_item(
            self,
            item: scrapy.Item,
            spider: scrapy.Spider,
    ) -> scrapy.Item:
        """
        Обрабатывает каждый элемент, подсчитывая количество документов
        в каждом статусе PEP.

        params:
            item (scrapy.Item): Объект, содержащий данные о PEP:
                - number (str): Номер PEP-документа.
                - name (str): Название PEP-документа.
                - status (str): Текущий статус PEP.
            spider (scrapy.Spider): Экземпляр паука, передающего элемент.

        return:
            scrapy.Item: Исходный объект item для передачи следующему pipeline.
        """
        # Получаем статус из item, если его нет — используем 'Unknown'
        status: str = item.get('status', 'Unknown')

        # Проверяем корректность статуса
        if not isinstance(status, str) or not status.strip():
            status = 'Unknown'
            self.logger.warning(
                f'[{spider.name}] PEP без корректного статуса: '
                f'{item.get("number", "неизвестно")}'
            )

        # Увеличиваем счётчик для данного статуса
        self._status_counts[status] += 1
        # Логирование
        self.logger.debug(
            f'[{spider.name}] Обработан PEP с статусом: {status}'
        )
        # Возвращаем элемент дальше по цепочке пайплайнов
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """
        Вызывается после завершения работы паука.
        Формирует CSV-файл со сводкой по статусам PEP-документов.

        params:
            spider (scrapy.Spider): Экземпляр паука, завершившего работу.
        return:
            None
        """
        if not self._status_counts:
            self.logger.warning(
                f'[{spider.name}] Не было обработано ни одного PEP.'
            )

        # Формируем имя файла с меткой времени
        now_str: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        summary_file: Path = self.output_dir / f'status_summary_{now_str}.csv'

        if not self.output_dir.exists():
            self.logger.error(
                f'[{spider.name}] Директория для CSV не существует: '
                f'{self.output_dir}'
            )
            return

        # Подсчитываем общее количество документов
        total_count: int = sum(self._status_counts.values())

        # Фильтруем некорректные статусы
        valid_statuses: dict[str, int] = {
            k: v
            for k, v in self._status_counts.items()
            if k and isinstance(k, str)
        }

        if len(valid_statuses) < len(self._status_counts):
            self.logger.warning(
                f'[{spider.name}] Некоторые статусы некорректны '
                'и были проигнорированы.'
            )

        # Записываем CSV
        try:
            with summary_file.open('w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Статус', 'Количество'])
                for status, count in sorted(valid_statuses.items()):
                    writer.writerow([status, count])
                writer.writerow(['Total', total_count])
        except Exception as e:
            self.logger.error(f'[{spider.name}] Ошибка при записи CSV: {e}')
            return

        # Проверка успешного создания CSV
        if summary_file.exists() and summary_file.stat().st_size > 0:
            self.logger.info(
                f'[{spider.name}] CSV успешно создан '
                f'({summary_file.stat().st_size} байт): {summary_file}'
            )
        else:
            self.logger.error(
                f'[{spider.name}] CSV пустой или не создан: {summary_file}'
            )

        self.logger.info(f'[{spider.name}] Всего документов: {total_count}')
