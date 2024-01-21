from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

## Создание подключения к базе данных
engine = create_engine('postgresql://')

## Создание сессии работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

## Объявление базовой модели данных
Base = declarative_base()

## Определение структуры таблицы "Книга"
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    publisher = Column(String)

## Определение структуры таблицы "Магазин"
class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String)

## Определение структуры таблицы "Покупка"
class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    price = Column(Integer)
    date = Column(Date)

    book = relationship("Book", backref="purchases")
    store = relationship("Store", backref="purchases")

## Получение имени или идентификатора издателя от пользователя
publisher = input("Введите имя или идентификатор издателя: ")

## Выполнение запроса выборки магазинов, продающих книги данного издателя
query = session.query(Book.name, Store.name, Purchase.price, Purchase.date)\
    .join(Purchase, Book.id == Purchase.book_id)\
    .join(Store, Store.id == Purchase.store_id)\
    .filter(Book.publisher == publisher)

# Вывод результатов запроса
for book_name, store_name, price, date in query:
    print(f"{book_name} | {store_name} | {price} | {date}")
