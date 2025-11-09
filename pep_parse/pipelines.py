from pathlib import Path
from datetime import datetime
import logging
from collections import Counter

import scrapy

from pep_parse import settings


class PepParsePipeline:
    """
    Pipeline собирает статистику по статусам PEP-документов
    и записывает сводный отчёт в файл csv.

    В файле два столбца:
    - Статус: название статуса PEP;
    - Количество: число документов с данным статусом;
    Строка файла Total содержит сумарное значение.
    """

    def __init__(self) -> None:
        """
        Инициализирует директорию для вывода результатов,
        создаёт внутренний словарь для подсчёта статусов.
        """
        # папка для сохранения результатов
        self.output_dir: Path = settings.RESULTS_DIR
        self.output_dir.mkdir(exist_ok=True)
        # словарь для подсчёта количества документов по статусу
        self.status_counter: Counter[str] = Counter()
        # логгер
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
        self.status_counter = Counter()

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
        # Получаем статус из item, если его нет то используем Unknown
        status: str = item.get('status', 'Unknown')

        # Проверяем корректность статуса
        if not isinstance(status, str) or not status.strip():
            status = 'Unknown'
            self.logger.warning(
                f'[{spider.name}] PEP без корректного статуса: '
                f'{item.get("number", "неизвестно")}'
            )

        # Увеличиваем счётчик для данного статуса
        self.status_counter[status] += 1

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
        if not self.status_counter:
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

        total_count: int = sum(self.status_counter.values())

        # Фильтруем некорректные статусы
        valid_statuses: dict[str, int] = {
            k: v
            for k, v in self.status_counter.items()
            if k and isinstance(k, str)
        }

        if len(valid_statuses) < len(self.status_counter):
            self.logger.warning(
                f'[{spider.name}] Некоторые статусы некорректны '
                'и были проигнорированы.'
            )

        try:
            # Формируем csv
            with summary_file.open('w', encoding='utf-8', newline='') as f:
                f.write('Статус,Количество\n')
                for st, cnt in valid_statuses.items():
                    f.write(f'{st},{cnt}\n')
                f.write(f'Total,{total_count}\n')
        except Exception as e:
            self.logger.error(f'[{spider.name}] Ошибка при записи CSV: {e}')
            return

        # Проверка создания CSV
        if summary_file.exists() and summary_file.stat().st_size > 0:
            self.logger.info(
                f'[{spider.name}] CSV успешно создан '
                f'({summary_file.stat().st_size} байт): {summary_file}'
            )
        else:
            self.logger.error(
                f'[{spider.name}] CSV пустой или не создан: {summary_file}'
            )
