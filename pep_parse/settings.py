"""
Настройки проекта Scrapy для парсинга PEP-документов.

Структура проекта:
    pep_parse/       - директория с кодом пауков
    results/         - директория для CSV-файлов с результатами
    tests/           - директория с тестами

Основные возможности:
- Сохранение списка всех PEP через Feeds (CSV)
- Сводка по статусам PEP через Pipeline (CSV)
- Соблюдение правил robots.txt
"""
from pathlib import Path

# Корневая директория проекта (один уровень выше текущего файла settings.py)
ROOT_PATH: Path = Path(__file__).parent.parent

# Расширение файлов CSV для сохранения результатов
DOC_EXTENSION: str = 'csv'

# Название папки, где будут сохраняться результаты парсинга
EXPORT_FOLDER: str = 'results'

# Полный путь к директории для сохранения CSV-файлов
RESULTS_DIR: Path = ROOT_PATH / EXPORT_FOLDER

# Префикс для файлов со сводкой по статусам PEP
PREFIX: str = 'status_summary'

# Имя бота Scrapy (идентификатор проекта)
BOT_NAME: str = 'pep_parse'

# Модули, где Scrapy ищет пауков
SPIDER_MODULES: list[str] = ['pep_parse.spiders']

# Модуль, куда создаются новые пауки через команду 'scrapy genspider'
NEWSPIDER_MODULE: str = 'pep_parse.spiders'

# Кодировка для экспорта данных через Feeds (CSV, JSON и т.д.)
FEED_EXPORT_ENCODING: str = 'utf-8'

# Настройки Feeds для автоматического сохранения списка PEP в CSV
FEEDS: dict[str, dict] = {
    'results/pep_%(time)s.csv': {  # Путь к файлу, %(time)s
        'format': 'csv',  # Формат сохраняемого файла
        'fields': ['number', 'name', 'status'],  # Порядок колонок в CSV
        'overwrite': True,  # Перезаписывать файл, если он уже существует
    }
}

# Соблюдать правила robots.txt на сайте при парсинге
ROBOTSTXT_OBEY: bool = True

# Настройка пайплайнов Scrapy
ITEM_PIPELINES: dict[str, int] = {
    'pep_parse.pipelines.PepParsePipeline': 300,  # Подсчёт статусов PEP
}

# Шаблон имени файла для сводки по статусам PEP
# %(time)s будет автоматически заменён на метку времени
PEP_STATUS_SUMMARY_FILENAME: str = 'status_summary_%(time)s.csv'
