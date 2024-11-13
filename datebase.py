# Импортирование необходимых компонентов для работы с SQLAlchemy
from sqlalchemy import (
    Column,  # Для создания колонок в таблицах
    Integer,  # Для целочисленных значений
    String,  # Для строковых значений
    Date,  # Для работы с типом данных Date
    ForeignKey,  # Для указания внешних ключей
    Table  # Для создания промежуточных таблиц
)
from sqlalchemy.ext.declarative import declarative_base  # Для базового класса моделей
from sqlalchemy import create_engine  # Для создания подключения к базе данных
from sqlalchemy.orm import sessionmaker  # Для создания сессии для работы с базой данных
from sqlalchemy.orm import relationship  # Для задания связей между моделями

# Создание базового класса для всех моделей
Base = declarative_base()

# Промежуточная таблица для связи между материалами и продукцией
materials_products = Table(
    'материалы_продукции', Base.metadata,
    Column('id_продукции', Integer, ForeignKey('продукция.id'), primary_key=True),  # Внешний ключ на таблицу продукции
    Column('id_материала', Integer, ForeignKey('материал.id'), primary_key=True)  # Внешний ключ на таблицу материалов
)

# Промежуточная таблица для связи между заявками и продукцией
product_request = Table(
    'заявка_продукции', Base.metadata,
    Column('id_заявки', Integer, ForeignKey('заявка.id'), primary_key=True),  # Внешний ключ на таблицу заявок
    Column('id_продукции', Integer, ForeignKey('продукция.id'), primary_key=True),  # Внешний ключ на таблицу продукции
    Column('количество_продукции', String),  # Количество продукции в заявке
    Column('стоимость', Date),  # Стоимость продукции на момент продажи
    Column('дата_продажи', String)  # Дата продажи
)

# Промежуточная таблица для связи между партнерами и продукцией в истории реализации
history_implementation = Table(
    "история_реализации", Base.metadata,
    Column('id_партнер', Integer, ForeignKey('партнер.id'), primary_key=True),  # Внешний ключ на таблицу партнеров
    Column('id_продукция', Integer, ForeignKey('продукция.id'), primary_key=True),  # Внешний ключ на таблицу продукции
    Column('количество', String),  # Количество реализованной продукции
    Column('дата_продажи', Date)  # Дата реализации продукции
)

# Модель для таблицы "тип_партнера"
class Type_partner(Base):
    __tablename__ = "тип_партнера"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    наименование = Column(String)  # Наименование типа партнера
    
    # Связь с партнерами, которые имеют данный тип
    партнер = relationship("Partner", back_populates="тип_партнера")

# Модель для таблицы "юридический_адрес"
class Legal_address(Base):
    __tablename__ = "юридический_адрес"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    индекс = Column(String)  # Почтовый индекс
    регион = Column(String)  # Регион
    город = Column(String)  # Город
    улица = Column(String)  # Улица
    дом = Column(String)  # Дом
    
    # Связь с партнерами, которые имеют данный юридический адрес
    партнер = relationship("Partner", back_populates="юридический_адрес")

# Модель для таблицы "поставщик"
class Supplier(Base):
    __tablename__ = "поставщик"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    наименование = Column(String)  # Наименование поставщика
    инн = Column(String)  # ИНН поставщика
    история_поставок = Column(String)  # История поставок
    
    # Связь с материалами, которые поставляются этим поставщиком
    материал = relationship("Material", back_populates="поставщик")

# Модель для таблицы "склад"
class Composition(Base):
    __tablename__ = "склад"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    поступления_материалов = Column(String)  # Поступления материалов на склад
    резерв_материалов = Column(String)  # Резерв материалов
    отпуск_материалов = Column(String)  # Отпуск материалов
    текущие_остатки = Column(String)  # Текущие остатки материалов на складе
    
    # Связь с материалами, которые находятся на этом складе
    материал = relationship("Material", back_populates="склад")

# Модель для таблицы "тип_материала"
class Material_type(Base):
    __tablename__ = "тип_материала"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    наименование = Column(String)  # Наименование типа материала
    процент_брака = Column(String)  # Процент брака для данного типа материала
    
    # Связь с материалами данного типа
    материал = relationship("Material", back_populates="тип_материала")

# Модель для таблицы "материал"
class Material(Base):
    __tablename__ = "материал"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    наименование = Column(String)  # Наименование материала
    id_поставщик = Column(Integer, ForeignKey("поставщик.id"))  # Внешний ключ на поставщика
    колво_в_упаковке = Column(String)  # Количество материала в упаковке
    id_склад = Column(Integer, ForeignKey("склад.id"))  # Внешний ключ на склад
    ед_измерения = Column(String)  # Единица измерения материала
    описание = Column(String)  # Описание материала
    стоимость = Column(String)  # Стоимость материала
    колво_на_складе = Column(String)  # Количество материала на складе
    мин_колво = Column(String)  # Минимальное количество на складе
    id_тип = Column(Integer, ForeignKey("тип_материала.id"))  # Внешний ключ на тип материала
    процент_брака = Column(String)  # Процент брака для этого материала

    # Связь с поставщиком, складом и типом материала
    поставщик = relationship("Supplier", back_populates="материал")
    склад = relationship("Composition", back_populates="материал")
    тип_материала = relationship("Material_type", back_populates="материал")

    # Связь с продукцией через промежуточную таблицу
    продукция = relationship("Products", secondary=materials_products, back_populates="материал")

# Модель для таблицы "тип_продукции"
class Product_type(Base):
    __tablename__ = "тип_продукции"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    наименование = Column(String)  # Наименование типа продукции
    коэф_типа_продукции = Column(String)  # Коэффициент типа продукции
    
    # Связь с продукцией данного типа
    продукция = relationship("Products", back_populates="тип_продукции")

# Модель для таблицы "продукция"
class Products(Base):
    __tablename__ = "продукция"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    id_тип = Column(Integer, ForeignKey("тип_продукции.id"))  # Внешний ключ на тип продукции
    наименование = Column(String)  # Наименование продукции
    описание = Column(String)  # Описание продукции
    мин_стоимость = Column(String)  # Минимальная стоимость продукции
    размер_упаковки = Column(String)  # Размер упаковки продукции
    вес_без_упаковки = Column(String)  # Вес продукции без упаковки
    вес_с_упаковкой = Column(String)  # Вес продукции с упаковкой
    сертификат_качества = Column(String)  # Номер сертификата качества
    номер_стандарта = Column(String)  # Номер стандарта продукции
    время_изготовления = Column(String)  # Время изготовления продукции
    себестоимость = Column(String)  # Себестоимость продукции
    колво_на_складе = Column(String)  # Количество продукции на складе

    # Связь с типом продукции
    тип_продукции = relationship("Product_type", back_populates="продукция")
        
    # Связь с заявкой через промежуточную таблицу
    заявка = relationship("Bid", secondary=product_request, back_populates="продукция")
    
    # Связь с материалами через промежуточную таблицу
    материал = relationship("Material", secondary=materials_products, back_populates="продукция")
    
    # Связь с партнереом через промежуточную таблицу
    партнер = relationship("Partner", secondary=history_implementation, back_populates="продукция")

class Partner(Base):
    # Таблица для хранения информации о партнерах
    __tablename__ = "партнер"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор партнера
    id_тип = Column(Integer, ForeignKey("тип_партнера.id"))  # Ссылка на тип партнера
    наименование = Column(String)  # Наименование партнера
    id_юр_адрес = Column(Integer, ForeignKey("юридический_адрес.id"))  # Ссылка на юридический адрес
    инн = Column(String)  # ИНН партнера
    фио_директора = Column(String)  # ФИО директора партнера
    телефон = Column(String)  # Телефон партнера
    email = Column(String)  # Email партнера
    рейтинг = Column(String)  # Рейтинг партнера
    места_продаж = Column(String)  # Места продаж продукции
    
    # Связи с другими таблицами
    заявка = relationship("Bid", back_populates="партнер")
    тип_партнера = relationship("Type_partner", back_populates="партнер")
    юридический_адрес = relationship("Legal_address", back_populates="партнер")
    
    # Связь с продукцией через промежуточную таблицу
    продукция = relationship("Products", secondary=history_implementation, back_populates="партнер")

class Pasport(Base):
    # Таблица для хранения паспортной информации сотрудников
    __tablename__ = "паспорт"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор паспорта
    серия = Column(String)  # Серия паспорта
    номер = Column(String)  # Номер паспорта
    кем_выдан = Column(String)  # Кем выдан паспорт
    дата_выдачи = Column(String)  # Дата выдачи паспорта

    сотрудник = relationship("Employee", back_populates="паспорт")


class Bank_details(Base):
    # Таблица для хранения банковских реквизитов сотрудников
    __tablename__ = "банковские_реквизиты"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор банковских реквизитов
    название_организации = Column(String)  # Название организации
    название_банка = Column(String)  # Название банка
    инн = Column(String)  # ИНН организации
    бик = Column(String)  # БИК банка
    корреспондентский_счет = Column(String)  # Корреспондентский счет

    сотрудник = relationship("Employee", back_populates="банковские_реквизиты")


class Job_title(Base):
    # Таблица для хранения информации о должностях сотрудников
    __tablename__ = "должность"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор должности
    наименование = Column(String)  # Наименование должности
    
    сотрудник = relationship("Employee", back_populates="должность")


class Employee(Base):
    # Таблица для хранения информации о сотрудниках
    __tablename__ = "сотрудник"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор сотрудника
    фамилия = Column(String)  # Фамилия сотрудника
    имя = Column(String)  # Имя сотрудника
    отчество = Column(String)  # Отчество сотрудника
    дата_рождения = Column(String)  # Дата рождения сотрудника
    id_паспорт = Column(Integer, ForeignKey("паспорт.id"))  # Ссылка на паспорт
    id_банк_реквизиты = Column(Integer, ForeignKey("банковские_реквизиты.id"))  # Ссылка на банковские реквизиты
    id_должность = Column(Integer, ForeignKey("должность.id"))  # Ссылка на должность
    наличие_семьи = Column(String)  # Информация о наличии семьи
    состояние_здоровья = Column(String)  # Информация о состоянии здоровья
    
    # Связи с другими таблицами
    паспорт = relationship("Pasport", back_populates="сотрудник")
    банковские_реквизиты = relationship("Bank_details", back_populates="сотрудник")
    должность = relationship("Job_title", back_populates="сотрудник")
    
    заявка = relationship("Bid", back_populates="сотрудник")
    
    перемещение = relationship("Moving", back_populates="сотрудник")


class Bid(Base):
    # Таблица для хранения информации о заявках
    __tablename__ = "заявка"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор заявки
    дата_создания = Column(String)  # Дата создания заявки
    статус = Column(String)  # Статус заявки
    id_партнер = Column(Integer, ForeignKey("партнер.id"))  # Ссылка на партнера
    id_сотрудник = Column(Integer, ForeignKey("сотрудник.id"))  # Ссылка на сотрудника
    предоплата = Column(String)  # Информация о предоплате
    дата_производства = Column(String)  # Дата производства
    согласована = Column(String)  # Информация о согласовании заявки
    
    # Связи с другими таблицами
    партнер = relationship("Partner", back_populates="заявка")
    сотрудник = relationship("Employee", back_populates="заявка")
    
    продукция = relationship("Products", secondary=product_request, back_populates="заявка")


class Premises(Base):
    # Таблица для хранения информации о помещениях
    __tablename__ = "помещение"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор помещения
    наименование = Column(String)  # Наименование помещения
    
    перемещение = relationship("Moving", back_populates="помещение")


class Moving(Base):
    # Таблица для хранения информации о перемещении сотрудников между помещениями
    __tablename__ = "перемещение"
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор перемещения
    id_сотрудник = Column(Integer, ForeignKey("сотрудник.id"))  # Ссылка на сотрудника
    id_помещение = Column(Integer, ForeignKey("помещение.id"))  # Ссылка на помещение
    дата_входа = Column(Date)  # Дата входа в помещение
    дата_выхода = Column(Date)  # Дата выхода из помещения
    
    сотрудник = relationship("Employee", back_populates="перемещение")
    помещение = relationship("Premises", back_populates="перемещение")


class Connect:
    # Класс для создания подключения к базе данных
    @staticmethod
    def create_connection():
        # Создание подключения к базе данных PostgreSQL
        engine = create_engine("postgresql://postgres:1234@localhost:5432/praktika")
        Base.metadata.create_all(engine)  # Создание всех таблиц в базе данных
        Session = sessionmaker(bind=engine)  # Создание сессии для работы с базой данных
        session = Session()  # Открытие сессии
        return session  #
