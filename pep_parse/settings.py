"""
Настройки проекта Scrapy для парсинга PEP-документов.
"""
from pathlib import Path

# Корневая директория проекта
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

# Модуль, куда создаются новые пауки
NEWSPIDER_MODULE: str = 'pep_parse.spiders'

# Кодировка для экспорта данных через Feeds
FEED_EXPORT_ENCODING: str = 'utf-8'

# Настройки Feeds
FEEDS: dict[str, dict] = {
    'results/pep_%(time)s.csv': {  # Путь к файл
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

# Настройки для паука PEP
SPIDER_PEP_NAME: str = 'pep'
SPIDER_PEP_ALLOWED_DOMAINS: list[str] = ['peps.python.org']
SPIDER_PEP_START_URLS: list[str] = ['https://peps.python.org/']
