# Управление продажами книг с использованием SQLAlchemy и PostgreSQL

## Описание проекта

Этот проект представляет собой систему управления данными о продажах книг с использованием ORM SQLAlchemy и базы данных PostgreSQL. Система хранит информацию об издателях, их книгах и фактах продажи. Книги могут продаваться в разных магазинах, поэтому учитывается не только, какая книга была продана, но и в каком магазине это произошло, а также когда.

## Структура проекта

Проект включает следующие файлы:

- **home_work.py** - основной скрипт для создания таблиц, заполнения тестовыми данными и выполнения запросов к базе данных.
- **fixtures/tests_data.json** - файл с тестовыми данными для заполнения базы данных.

## Описание моделей данных

### Publisher (Издатель)

- **id** (Integer, primary_key) - Идентификатор издателя
- **name** (String, уникальное) - Имя издателя

### Book (Книга)

- **id** (Integer, primary_key) - Идентификатор книги
- **title** (Text, не может быть пустым) - Название книги
- **id_publisher** (Integer, ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False) - Идентификатор издателя

### Shop (Магазин)

- **id** (Integer, primary_key) - Идентификатор магазина
- **name** (String, уникальное) - Название магазина

### Stock (Запас)

- **id** (Integer, primary_key) - Идентификатор запаса
- **id_book** (Integer, ForeignKey('book.id', ondelete='CASCADE'), nullable=False) - Идентификатор книги
- **id_shop** (Integer, ForeignKey('shop.id', ondelete='CASCADE'), nullable=False) - Идентификатор магазина
- **count** (Integer, nullable=False) - Количество книг на складе

### Sale (Продажа)

- **id** (Integer, primary_key) - Идентификатор продажи
- **price** (Integer, nullable=False) - Цена продажи
- **date_sale** (Date, nullable=False) - Дата продажи
- **count** (Integer, nullable=False) - Количество проданных книг
- **id_stock** (Integer, ForeignKey('stock.id', ondelete='CASCADE'), nullable=False) - Идентификатор запаса