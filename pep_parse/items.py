"""
pep_parse/items.py

Определяет структуру данных для Scrapy-паука `PepSpider`.

Каждый объект PepParseItem представляет один PEP-документ и хранит:
    - number: номер PEP-документа (str)
    - name: название документа (str)
    - status: текущий статус документа (str)

Также реализован метод __repr__ для удобного вывода объекта в логах
или интерактивной отладке.
"""
import scrapy


class PepParseItem(scrapy.Item):
    """
    Описание структуры данных для парсинга PEP-документов.

    Каждый объект этого класса представляет собой один документ PEP
    и используется для хранения данных, собранных пауком.

    Атрибуты:
        number (scrapy.Field): Номер PEP-документа (например, '8', '484').
        name (scrapy.Field): Название PEP-документа (короткое описание).
        status (scrapy.Field): Текущий статус PEP (например, 'Active').
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

    def __repr__(self) -> str:
        """
        Возвращает удобное строковое представление объекта для отладки.
        Например: <PepParseItem PEP 8: 'Style Guide for Python Code' (Active)>
        """
        num = self.get('number', '?')
        name = self.get('name', 'Unknown')
        status = self.get('status', 'Unknown')
        return f"<PepParseItem PEP {num}: '{name}' ({status})>"
