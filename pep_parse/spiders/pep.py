import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Паук для парсинга списка всех PEP (Python Enhancement Proposals).

    1. Начинает с главной страницы https://peps.python.org/.
    2. Собирает ссылки на страницы всех PEP.
    3. Переходит по каждой ссылке и извлекает:
       - Номер PEP-документа;
       - Название PEP-документа;
       - Текущий статус PEP.
    """
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """
        Собирает ссылки на страницы всех PEP со страницы каталога.
        Для каждой найденной ссылки вызывает метод parse_pep().
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
        Парсит страницу конкретного PEP и извлекает данные:
        - Номер PEP-документа;
        - Название PEP-документа;
        - Текущий статус PEP.
        Возвращает экземпляр PepParseItem.
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
