# Асинхронный парсер PEP

Проект **scrapy_parser_pep** — это асинхронный парсер на базе фреймворка **Scrapy**, предназначенный для автоматического сбора информации о документах PEP (Python Enhancement Proposals) с официального сайта [peps.python.org](https://peps.python.org/).

Парсер извлекает номера, названия и статусы всех документов PEP, сохраняет полученные данные в CSV-файлы и формирует сводную таблицу по количеству документов в каждом статусе.


### Основные функции

Парсер автоматически:
1. Собирает со стартовой страницы **все ссылки** на документы PEP.
2. Переходит по каждой из них и извлекает:
   - номер PEP,
   - название,
   - статус документа.
3. Сохраняет результаты в CSV-файл формата:
`results/pep_YYYY-MM-DD_HH-MM-SS.csv`
где указаны все собранные документы.
4. Формирует **сводную таблицу** по статусам PEP в отдельном CSV-файле:
`results/status_summary_YYYY-MM-DD_HH-MM-SS.csv`
с подсчётом количества документов каждого статуса и итоговой строкой `Total`.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/levinadev/scrapy_parser_pep.git
cd scrapy_parser_pep
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:
```
scrapy crawl pep
```

После завершения работы в директории results/ появятся два CSV-файла:

- pep_YYYY-MM-DD_HH-MM-SS.csv — список всех PEP.
- status_summary_YYYY-MM-DD_HH-MM-SS.csv — сводка по статусам.


### Используемые технологии

- **Python 3.9**
- **Scrapy** — асинхронный фреймворк для парсинга данных.
- **CSV** — формат хранения результатов парсинга.
- **Pathlib** — работа с путями к файлам.
- **collections.defaultdict** — для подсчёта количества PEP по статусам.
- **logging** — для ведения логов и отслеживания процесса работы приложения.

### Автор

- Имя: Анна
- Email: anna45dd@yandex.ru
- GitHub: https://github.com/levinadev
