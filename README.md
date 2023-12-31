# Сервис для сбора информации о посещаемых доменах

### Краткое описание

В данном репозитории размещен код для веб-сервиса контроля посещенных сотрудниками компании веб-сайтов.

- сервис построен на основе асинхронного фреймворка FastAPI;
- для формирования базы данных применено решение PostgreSQL, запускаемый из Docker-контейнера;
- обращение к базе посредством ORM SQLAlchemy;
- для автотестирования работы сервера применяется библиотека Pytest;
- логирование ведется с помощью стандартной библиотеки logging;
- секреты для запуска берутся из файла .env.

В текущей версии сформированы 3 ендпоинта:
- для направления на сервер списка посещенных сайтов, которые далее записываются в базу данных (PostgreSQL в Docker-контейнере);
- для получения списка имеющихся в базе данных об уникальных доменах, посещенных сотрудниками. Опционально с помощью query-параметров time_from и time_to можно задавать период, за который необходимо получать данные - int-число в секундах "от начала эпохи". В случае отсутствия одного из параметров соответствующее ему ограничение не применяется.

### Инструкция для запуска и тестирования сервиса:
    
- клонировать репозиторий на свою рабочую станцию с помощью команды `git clone https://github.com/Konstantin-Chemesov/web_sites_control.git`;
- с помощью команды `pip install -r requirements.txt` установить неоюходимые для работы библиотеки;
- в папке с проектом создать файл с именем .env, в него объявить следующие переменные окружения:

DB_NAME = "db_links"
DB_USERNAME = <database username>
DB_PASSWORD = <database password>
DB_PORT = "5432"
PROJECT_HOST = "0.0.0.0"
PROJECT_PORT = '8000'

- командой `docker-compose up` из директории с проектом запустить контейнер с базой данных;
- в терминал ввести строку `python3 src/main.py` для запуска работы сервера;
- при помощи программы Postman направить http-запросы на сервер. В файле links_control.postman_collection.json находится коллекция запросов, предназначенных для тестирования работы системы.