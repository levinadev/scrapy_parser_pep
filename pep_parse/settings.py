from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_FORMAT = 'csv'

EXPORT_FOLDER = 'results'
RESULTS_DIR = ROOT_PATH / EXPORT_FOLDER


SUMMARY_NAME = 'status_summary'
SUMMARY_TABLE_HEADER = ('Status', 'Quantity')
SUMMARY_TABLE_BOTTOM = 'Total'
BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    }
}

FEED_EXPORT_FIELDS = ['number', 'name', 'status']

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

PEP_STATUS_SUMMARY_FILENAME = 'status_summary_%(time)s.csv'