import scrapy


class PepParseItem(scrapy.Item):
    """
    Описание структуры данных для парсинга PEP-документов.
    """
    number = scrapy.Field(
        description='Номер PEP-документа'
    )
    name = scrapy.Field(
        description='Название PEP-документа'
    )
    status = scrapy.Field(
        description='Текущий статус PEP'
    )
