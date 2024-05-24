from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json
from datetime import date

DSN = 'postgresql://postgres:20145@localhost:5432/ORM_HomeWork'

engine = create_engine(DSN)
Base = declarative_base()


# Издатель - Publisher
class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"

# Книга - Book
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    
    id_publisher = Column(Integer, ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)
    publisher = relationship("Publisher", backref="books")

    def __str__(self):
        return f"{self.id}: {self.title}"

# Магазин - Shop
class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"



class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship("Book", backref="stock")
    shop = relationship("Shop", backref="stock")

    def __str__(self):
        return f"{self.id}: ({self.id_book} {self.id_shop} {self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(Date, nullable=False)
    count = Column(Integer, nullable=False)

    id_stock = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    stock = relationship("Stock", backref="sales")

    def __str__(self):
        return f"{self.id}: ({self.id_stock} {self.price} {self.date_sale} {self.count})"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def fill_data(session):
    # Добавление издателей
    publisher1 = Publisher(name='Пушкин')
    session.add(publisher1)
    session.commit()

    # Добавление книг
    book1 = Book(title='Капитанская дочка', id_publisher=publisher1.id)
    book2 = Book(title='Руслан и Людмила', id_publisher=publisher1.id)
    book3 = Book(title='Евгений Онегин', id_publisher=publisher1.id)
    session.add_all([book1, book2, book3])
    session.commit()

    # Добавление магазинов
    shop1 = Shop(name='Буквоед')
    shop2 = Shop(name='Лабиринт')
    shop3 = Shop(name='Книжный дом')
    session.add_all([shop1, shop2, shop3])
    session.commit()

    # Добавление запасов (Stock)
    stock1 = Stock(id_book=book1.id, id_shop=shop1.id, count=5)
    stock2 = Stock(id_book=book2.id, id_shop=shop1.id, count=3)
    stock3 = Stock(id_book=book1.id, id_shop=shop2.id, count=8)
    stock4 = Stock(id_book=book3.id, id_shop=shop3.id, count=6)
    stock5 = Stock(id_book=book1.id, id_shop=shop1.id, count=10)
    session.add_all([stock1, stock2, stock3, stock4, stock5])
    session.commit()

    # Добавление продаж (Sale)
    sale1 = Sale(price=600, date_sale=date(2022, 11, 9), count=1, id_stock=stock1.id)
    sale2 = Sale(price=500, date_sale=date(2022, 11, 8), count=1, id_stock=stock2.id)
    sale3 = Sale(price=580, date_sale=date(2022, 11, 5), count=1, id_stock=stock3.id)
    sale4 = Sale(price=490, date_sale=date(2022, 11, 2), count=1, id_stock=stock4.id)
    sale5 = Sale(price=600, date_sale=date(2022, 10, 26), count=1, id_stock=stock5.id)
    session.add_all([sale1, sale2, sale3, sale4, sale5])
    session.commit()

create_tables(engine)

Session = sessionmaker(bind = engine)
session = Session()

# Задание 3: Заполнение базы данных из json-файла
with open('fixtures/tests_data.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)

i = 0

for record in data:
    i += 1
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

    print(f'Запись {i} добавлена в таблицу {record.get("model")}')

session.commit()

# Заполнение базы данных по данным из файла (закоментировали код,
# так как данные беруться из fixtures/tests_data.json)
# fill_data(session)

# Задание 2: Прием имени или идентификатора издателя
publisher_name_or_id = input("Введите имя или идентификатор издателя: ")

# Поиск издателя по имени или идентификатору
if publisher_name_or_id.isdigit():
    publisher = session.query(Publisher).filter(Publisher.id == int(publisher_name_or_id)).first()
else:
    publisher = session.query(Publisher).filter(Publisher.name == publisher_name_or_id).first()

if publisher is None:
    print("Издатель не найден")
else:
    results = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).
        join(Stock, Book.id == Stock.id_book).
        join(Sale, Stock.id == Sale.id_stock).
        join(Shop, Stock.id_shop == Shop.id).
        filter(Book.id_publisher == publisher.id).all()
        )

    for title, shop_name, price, date_sale in results:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")


session.close()