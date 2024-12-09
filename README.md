# Учебный проект Python/DjangoDRF
## Описание
Разработка LMS-системы, в которой каждый желающий может размещать свои полезные материалы или курсы.
## Задачи
### 30.1 Вьюсеты и дженерики
1. Создать новый Django-проект, подключить DRF в настройках проекта.
2. Создать модели:
	* Пользователь (авторизацию заменить на email. Добавить поля: телефон, город, аватар.)
	* Курс (Поля: название, описание, превью.)
	* Урок (Поля: название, описание, превью, сылка на видео.)
3. Описать CRUD для моделей курса и урока с использованием Viewsets и Generic классы.
### 30.2 Сериализаторы
1. Для модели курса добавить в сериализатор поле вывода количества уроков.
2. Добавить модель «Птатежи» в приложение users с полями:
	* Пользователь
	* Дата оплаты
	* Оплаченный курс или урок
	* Сумма оплаты
	* Способ оплаты: наличные или перевод на счет.
3. Для сериализатора для модели курса реализовать поле вывода уроков.
4. Настроить фильтрацию для эндпоинта вывода списка платежей с возможностями:
	* Менять порядок сортировки по дате оплаты
	* Фильтровать по курсу или уроку
	* Фильтровать по способу оплаты.
### 31 Права доступа в DRF
1. Реализовать CRUD для пользователей, в том числе регистрацию пользователей.
	Настроить в проекте использование JWT-авторизации и закрыть каждый эндпоинт авторизацией.
2. Завести группу модераторов и опишисать для нее права работы с любыми уроками и курсами,
	но без возможности их удалять и создавать новые.
3. Описать права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов,
	могли видеть, редактировать и удалять только свои курсы и уроки.
### 32.1 Валидаторы, пагинация и тесты
1. Для сохранения уроков и курсов реализовать дополнительную проверку на отсутствие в материалах
	ссылок на сторонние ресурсы, кроме youtube.com.
2. Добавить модель подписки на обновления курса для пользователя.
	Реализовать эндпоинт для установки и удаления подписки у пользователя.
3. Реализовать пагинацию для вывода всех уроков и курсов.
4. Написать тесты, которые будут проверять корректность работы CRUD уроков
	и функционал работы подписки на обновления курса.
### 32.2 Документирование и безопвсность
1. Подключить и настроить вывод документации для проекта.
2. Подключить возможность оплаты курсов через https://stripe.com/docs/api.
### 33 Celery
1. Настроbnm проект для работы с Celery и celery-beat для выполнения периодических задач.
2. Добавить асинхронную рассылку писем пользователям об обновлении материалов курса.
3. Реализовать фоновую задачу, которая будет проверять пользователей по дате последнего входа по полю last_login
    и, если пользователь не заходил более месяца, блокировать его с помощью флага is_active.
## Линтеры
* `flake8`
* `black`
* `mypy`
* `isort`
* `django-stubs`
* `djangorestframework-stubs`
* `types-psycopg2`
* `django-filter-stubs`
## Зависимости
* `django`
* `djangorestframework`
* `python-dotenv`
* `ipython`
* `pillow`
* `redis`
* `psycopg2-binary`
* `django-filter`
* `djangorestframework-simplejwt`
* `drf-yasg`
* `stripe`
* `django-cors-headers`
* `celery`
* `django-celery-beat`
## Установка
1. Клонировать проект
	```
	<https://github.com/Ramazan-Z/DRF_Project.git>
	```
2. Установить зависимости
	```
	poetry install
	```
3. Создать в корне проекта файл `.env` из  копии `env.example`и прописать в нем:
	* Секретный ключ и флаг дебага проекта
	* Параметры для подключения к базе данных.
    * Токен платежной системы Stripe
    * URL-адрес брокера сообщений Redis
    * Настройки почтового сервера
4. Создать базу данных, ее стуктуру и наполнить тестовыми данными:
	```
	python manage.py start_test_db
	```
 5. Запустить Celery
    ```
	celery -A config worker -l INFO
	```
6. Запустить Celery-beat
    ```
	celery -A config beat -l INFO
	```
## Тестирование
	* Запуск теста: `coverage run --source='.' manage.py test`
	* Покрытие кода: `coverage report`
## Запуск
```
python manage.py runserver
```