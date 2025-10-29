import scrapy
from urllib.parse import urljoin
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse(self, response):
        """
        Метод парсит стартовую страницу и собирает ссылки на документы PEP.
        """
        # Находим все строки таблицы с PEP (кроме заголовка)
        # Предполагаем, что таблица одна или все нужные ссылки находятся в
        # общем селекторе:
        pep_links = response.css('section#index-by-category table.pep-index tbody tr')

        for pep_link in pep_links:
            # Извлекаем относительную ссылку на документ PEP
            relative_url = pep_link.css('td a::attr(href)').get()

            # Если ссылки нет, пропускаем
            if not relative_url:
                continue

            # Формируем полную ссылку
            full_url = urljoin(response.url, relative_url)

            # Отправляем запрос на страницу PEP для парсинга
            yield response.follow(full_url, callback=self.parse_pep)

    def parse_pep(self, response):
        """
        Метод парсит страницы с документами PEP и формирует Items.
        """
        # Селектор для извлечения номера (например, 8) и имени (например, The Style Guide for Python Code)
        # Номер находится в заголовке, например: #PEP 8 – The Style Guide for Python Code
        title = response.css('h1.page-title::text').get().strip()

        # Регулярное выражение или разбор строки для извлечения номера и имени
        # Пример: 'PEP 8 – The Style Guide for Python Code'
        try:
            # Извлекаем номер и имя
            number_str, name = title.split(' – ', 1)
            number = number_str.split()[1]  # Берем "8" из "PEP 8"
        except ValueError:
            # Обработка случаев, когда заголовок не в ожидаемом формате
            self.logger.warning(f"Не удалось распарсить заголовок PEP на странице {response.url}: {title}")
            return

        # Селектор для извлечения статуса
        # Статус находится в метаданных: <dt>Status</dt><dd><abbr title="Final">Final</abbr></dd>
        status = response.css('dt:contains("Status") + dd abbr::text').get()

        if status:
            status = status.strip()

        # Создаем и заполняем Item
        pep_item = PepParseItem(
            number=number,
            name=name,
            status=status
        )

        yield pep_item
