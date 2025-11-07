from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
TIME_PATTERN = '%Y-%m-%d_%H-%M-%S'
DOC_EXTENSION = 'csv'

EXPORT_FOLDER = 'results'
RESULTS_DIR = ROOT_PATH / EXPORT_FOLDER

PREFIX = 'status_summary'
TABLE_HEADINGS = ('Status', 'Quantity')
TOTAL_TAG = 'Total'

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
