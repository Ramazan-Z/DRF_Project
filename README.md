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
4. Создать базу данных, ее стуктуру и наполнить тестовыми данными:
	```
	python manage.py start_test_db
	```
## Запуск
```
python manage.py runserver
```