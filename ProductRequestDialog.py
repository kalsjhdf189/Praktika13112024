from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QWidget
)
from datebase import history_implementation, Products, Partner  # Импортируем модели для работы с базой данных
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

class ProductRequestDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)  # Инициализация родительского класса QDialog
        self.setWindowTitle("Реализация продукции")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('icon.ico'))  # Устанавливаем иконку окна
        self.setGeometry(100, 100, 800, 600)  # Устанавливаем начальные размеры окна
        self.session = session  # Сессия для работы с базой данных
        self.init_ui()  # Инициализируем интерфейс

    def init_ui(self):
        # Логотип для окна
        logo_label = QLabel()  # Создаем метку для логотипа
        logo_pixmap = QPixmap('logotype.png').scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)  # Загружаем логотип и задаем его размер
        logo_label.setPixmap(logo_pixmap)  # Устанавливаем логотип

        # Заголовок окна
        app_title = QLabel("Реализация продукции")  # Текст заголовка
        app_title.setStyleSheet("font-family: SegoeUI; font-size: 18px; font-weight: bold; text-align: left;")  # Стиль для заголовка

        # Основной layout для окна
        layout = QVBoxLayout(self)

        # Создаем таблицу для отображения данных
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Устанавливаем количество колонок
        self.table.setHorizontalHeaderLabels(["Партнер", "Продукция", "Количество", "Дата продажи"])  # Устанавливаем заголовки колонок
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Делаем таблицу доступной только для чтения

        # Загружаем данные для отображения в таблице
        self.load_history_implementation()
        
        # Кнопка для закрытия окна
        close_button = self.create_button("Назад", self.open_main_window)

        # Верхний header с логотипом и заголовком
        header_widget = QWidget()  # Создаем виджет для шапки окна
        header_widget.setStyleSheet("background-color: #F4E8D3;")  # Задаем фон для шапки
        header_layout = QHBoxLayout(header_widget)  # Горизонтальный layout для шапки
        header_layout.addWidget(logo_label)  # Добавляем логотип
        header_layout.addWidget(app_title)  # Добавляем заголовок

        # Составляем общий layout окна
        layout.addWidget(header_widget)  # Добавляем шапку в основной layout
        layout.addWidget(self.table)  # Добавляем таблицу
        layout.addWidget(close_button)  # Добавляем кнопку для закрытия окна

    # Метод для создания кнопки с заданным текстом и обработчиком
    def create_button(self, text, handler):
        button = QPushButton(text)  # Создаем кнопку
        button.setStyleSheet("font-family: SegoeUI; background-color: #67BA80; color: white; border-radius: 5px; padding: 10px;")  # Стиль кнопки
        button.clicked.connect(handler)  # Подключаем обработчик для нажатия
        return button
    
    def open_main_window(self):
        from main_window import MainWindow
        # Закрытие текущего окна (ProductRequestDialog)
        self.close()
        
        # Открытие главного окна
        self.main_window = MainWindow()
        self.main_window.show()

    # Метод для загрузки данных о реализации продукции в таблицу
    def load_history_implementation(self):
        # Выполняем запрос к базе данных для получения данных о реализации
        history_data = self.session.query(
            history_implementation,  # История реализации
            Partner.наименование.label('partner_name'),  # Название партнера
            Products.наименование.label('product_name')  # Название продукции
        ).join(Partner, history_implementation.c.id_партнер == Partner.id).join(Products, history_implementation.c.id_продукция == Products.id).all()# Присоединяем таблицу продукции, партнеров и получаем все записи

        # Устанавливаем количество строк в таблице, равное количеству полученных данных
        self.table.setRowCount(len(history_data))

        # Заполняем таблицу данными
        for row, record in enumerate(history_data):
            partner_name = record.partner_name or "Неизвестно"  # Если имя партнера отсутствует, выводим "Неизвестно"
            product_name = record.product_name or "Неизвестно"  # Если имя продукции отсутствует, выводим "Неизвестно"
            # Заполняем каждую ячейку таблицы
            self.table.setItem(row, 0, QTableWidgetItem(partner_name))  # Имя партнера
            self.table.setItem(row, 1, QTableWidgetItem(product_name))  # Имя продукции
            self.table.setItem(row, 2, QTableWidgetItem(str(record.количество)))  # Количество продукции
            self.table.setItem(row, 3, QTableWidgetItem(str(record.дата_продажи)))  # Дата продажи