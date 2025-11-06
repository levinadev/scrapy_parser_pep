import scrapy


class PepParseItem(scrapy.Item):
    """
    Описание структуры данных для парсинга PEP-документов.
    Каждый объект этого класса представляет один PEP.
    """
    number = scrapy.Field(
        desciption='Номер PEP-документа'
    )
    name = scrapy.Field(
        description='Название PEP-документа'
    )
    status = scrapy.Field(
        description='Текущий статус PEP'
    )
