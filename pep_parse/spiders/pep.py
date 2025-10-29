import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """
        Метод парсит стартовую страницу и собирает ссылки на документы PEP.
        """

        links = response.css('a[href^="pep-"]::attr(href)').getall()

        link_count = 0
        for link in links:
            if link.lower().endswith('pep-0000/'):
                continue

            link_count += 1
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """
        Метод парсит страницы с документами PEP и формирует Items.
        """

        title = response.css('h1.page-title::text').get()
        if not title:
            self.logger.warning("Нет h1.page-title, пропуск Item")
            return

        title = title.strip()

        try:
            number_str, name = title.split(' – ', 1)
            number = number_str.split()[1]
        except ValueError:
            self.logger.warning(
                f"Ошибка парсинга заголовка PEP на {response.url}: {title}. "
                "Ожидался формат 'PEP N – Name'."
            )
            return

        status = response.css('dt:contains("Status") + dd abbr::text').get()

        if status:
            status = status.strip()
        else:
            self.logger.warning(f"Статус не найден на странице {response.url}")
            status = 'не указан'

        self.logger.info(
            f"PEP {number} | {status} | {name[:40]}..."
        )

        pep_item = PepParseItem(
            number=number,
            name=name,
            status=status
        )

        yield pep_item
