import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """
        Метод парсит стартовую страницу и собирает ссылки на документы PEP.
        Используется альтернативный селектор, ищущий все ссылки на PEP.
        """
        self.logger.info('--- Начинаем парсинг стартовой страницы ---')

        links = response.css('a[href^="pep-"]::attr(href)').getall()

        self.logger.debug(f'Найдено потенциальных ссылок на PEP: {len(links)}')

        link_count = 0
        for link in links:
            if link.lower().endswith('pep-0000/'):
                continue

            link_count += 1
            yield response.follow(link, callback=self.parse_pep)

        self.logger.info(f'--- Завершено сканирование стартовой страницы. Отправлено запросов на PEP: {link_count} ---')

    def parse_pep(self, response):
        """
        Метод парсит страницы с документами PEP и формирует Items.
        """
        self.logger.debug(f'Обработка страницы: {response.url}')

        title = response.css('h1.page-title::text').get()
        if not title:
            self.logger.warning(f"Не найден заголовок h1.page-title на странице {response.url}. Item не будет создан.")
            return

        title = title.strip()

        try:
            number_str, name = title.split(' – ', 1)
            number = number_str.split()[1]
        except ValueError:
            self.logger.warning(
                f"Не удалось распарсить заголовок PEP на странице {response.url}: {title}. Ожидается 'PEP N – Name'.")
            return

        status = response.css('dt:contains("Status") + dd abbr::text').get()

        if status:
            status = status.strip()
        else:
            self.logger.warning(f"Статус не найден на странице {response.url}")
            status = 'не указан'  # Устанавливаем статус по умолчанию, если не нашли

        self.logger.info(f'--- СПАРШЕНО: PEP {number} | Статус: {status} | Название: {name[:40]}... ---')

        pep_item = PepParseItem(
            number=number,
            name=name,
            status=status
        )

        yield pep_item
