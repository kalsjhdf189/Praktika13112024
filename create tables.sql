create table тип_партнера (
id serial primary key,
наименование varchar(50)
);

create table юридический_адрес (
id serial primary key,
индекс int,
регион varchar(50),
город varchar(50),
улица varchar(50),
дом int
);

create table поставщик (
id serial primary key,
наименование varchar(50),
инн varchar(12),
история_поставок varchar(50)
);

create table склад (
id serial primary key,
поступления_материалов varchar(50),
резерв_материалов varchar(50),
отпуск_материалов varchar(50),
текущие_остатки varchar(50)
);

create table тип_материала (
id serial primary key,
наименование varchar(50),
процент_брака float
);

create table материал (
id serial primary key,
наименование varchar(50),
id_поставщик int,
колво_в_упаковке int,
id_склад int,
ед_измерения varchar(50),
описание varchar(255),
стоимость int,
колво_на_складе int,
мин_колво int,
id_тип int,
процент_брака decimal(3,2),
foreign key (id_тип) references тип_материала(id),
foreign key (id_поставщик) references поставщик(id),
foreign key (id_склад) references склад(id)
);

create table тип_продукции (
id serial primary key,
наименование varchar(50),
коэф_типа_продукции float
);

create table продукция (
id serial primary key,
id_тип int,
наименование varchar(100),
описание varchar(100),
мин_стоимость float,
размер_упаковки varchar(100),
вес_без_упаковки int,
вес_с_упаковкой int,
сертификат_качества varchar(100),
id_материал int,
номер_стандарта int,
время_изготовления date,
себестоимость float,
колво_на_складе int,
FOREIGN KEY (id_тип) REFERENCES тип_продукции(id),
FOREIGN KEY (id_материал) references материал(id)
);

create table партнер (
id serial primary key,
id_тип int,
наименование varchar(50),
id_юр_адрес int,
инн varchar(12),
фио_директора varchar(50),
телефон varchar(20),
email varchar(30),
рейтинг int,
места_продаж varchar(50),
foreign key (id_тип) references тип_партнера(id),
foreign key (id_юр_адрес) references юридический_адрес(id)
);

create table история_реализации (
id_партнер int,
id_продукция int,
количество int,
дата_продажи date,
primary key(id_партнер, id_продукция),
foreign key(id_партнер) references партнер(id) on delete cascade,
foreign key(id_продукция) references продукция(id) on delete cascade
);

create table паспорт (
id serial primary key,
серия int,
номер int,
кем_выдан varchar(50),
дата_выдачи date
);

create table банковские_реквизиты (
id serial primary key,
название_организации varchar(50),
название_банка varchar(50),
инн varchar(12),
бик int,
корреспондентский_счет varchar(50)
);

create table должность (
id serial primary key,
наименование varchar(50)
);

create table сотрудник (
id serial primary key,
фамилия varchar(50),
имя varchar(50),
отчество varchar(50),
дата_рождения date,
id_паспорт int,
id_банк_реквизиты int,
id_должность int,
наличие_семьи boolean,
состояние_здоровья varchar(50),
foreign key (id_должность) references должность(id),
foreign key (id_паспорт) references паспорт(id),
foreign key (id_банк_реквизиты) references банковские_реквизиты(id)
);

create table заявка (
id serial primary key,
дата_создания date,
статус varchar(50),
id_партнер int,
id_сотрудник int,
предоплата float,
дата_производства date,
согласована boolean,
foreign key (id_партнер) references партнер(id),
foreign key (id_сотрудник) references сотрудник(id)
);

create table помещение (
id serial primary key,
наименование varchar(50)
);

create table перемещение (
id serial primary key,
id_сотрудник int,
id_помещение int,
дата_входа date,
дата_выхода date,
foreign key (id_сотрудник) references сотрудник(id),
foreign key (id_помещение) references помещение(id)
);

create table материалы_продукции (
id_продукции int,
id_материала int,
primary key(id_продукции, id_материала),
foreign key (id_продукции) references продукция(id) on delete cascade,
foreign key (id_материала) references материал(id) on delete cascade
);

create table заявка_продукции (
id_заявки int,
id_продукции int,
количество_продукции int,
стоимость float,
дата_производства date,
primary key(id_заявки, id_продукции),
foreign key (id_заявки) references заявка(id) on delete cascade,
foreign key (id_продукции) references продукция(id) on delete cascade
)
