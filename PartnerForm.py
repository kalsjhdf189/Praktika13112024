from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox, QPushButton,
    QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget
)
from PySide6.QtCore import Qt, Signal
from datebase import Partner, Type_partner, Legal_address, Connect
from PySide6.QtGui import QPixmap, QIcon

class PartnerForm(QDialog):
    partner_added = Signal()  # Сигнал, который будет отправлен при добавлении или редактировании партнера

    def __init__(self, partner=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать партнера")  # Заголовок окна
        self.setWindowIcon(QIcon('icon.ico'))  # Устанавливаем иконку окна
        self.setGeometry(200, 200, 400, 300)  # Устанавливаем начальные размеры окна

        self.partner = partner  # Если редактируем, передаем объект партнера
        self.session = Connect.create_connection()  # Создаем подключение к базе данных
        self.init_ui()  # Инициализация пользовательского интерфейса

    def init_ui(self):
        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap('logotype.png')  # Загружаем логотип
        logo_pixmap = logo_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем логотип
        logo_label.setPixmap(logo_pixmap)  # Устанавливаем логотип на метке
        
        # Заголовок формы
        app_title = QLabel("Добавление/редактирование")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold;")  # Стиль заголовка

        # Создаем форму для ввода данных
        form_layout = QFormLayout()

        # Поля формы с заполнением, если партнер передан для редактирования
        self.name_input = QLineEdit(self.partner.наименование if self.partner else "")
        self.name_input.setPlaceholderText("Наименование")  # Устанавливаем текст-подсказку

        self.type_input = QComboBox()  # Выпадающий список типов партнеров
        self.type_input.addItems([tp.наименование for tp in self.session.query(Type_partner).all()])  # Получаем все типы из базы данных

        self.address_input = QComboBox()  # Выпадающий список юридических адресов
        self.address_input.addItems([f"{addr.город}, {addr.улица}, {addr.дом}" for addr in self.session.query(Legal_address).all()])  # Все адреса из базы данных

        # Поля для других данных
        self.inn_input = QLineEdit(self.partner.инн if self.partner else "")
        self.inn_input.setPlaceholderText("ИНН")
        self.director_input = QLineEdit(self.partner.фио_директора if self.partner else "")
        self.director_input.setPlaceholderText("ФИО директора")
        self.phone_input = QLineEdit(self.partner.телефон if self.partner else "")
        self.phone_input.setPlaceholderText("Телефон")
        self.email_input = QLineEdit(self.partner.email if self.partner else "")
        self.email_input.setPlaceholderText("Email")
        self.rating_input = QSpinBox()  # Спиннер для рейтинга
        self.rating_input.setRange(0, 10)  # Рейтинг от 0 до 10
        self.rating_input.setValue(int(self.partner.рейтинг) if self.partner and self.partner.рейтинг else 0)

        # Добавляем все поля в форму
        form_layout.addRow("Наименование", self.name_input)
        form_layout.addRow("Тип партнера", self.type_input)
        form_layout.addRow("Юридический адрес", self.address_input)
        form_layout.addRow("ИНН", self.inn_input)
        form_layout.addRow("ФИО Директора", self.director_input)
        form_layout.addRow("Телефон", self.phone_input)
        form_layout.addRow("Email", self.email_input)
        form_layout.addRow("Рейтинг", self.rating_input)

        # Кнопка для сохранения
        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet("background-color: #67BA80; color: white; border-radius: 5px; padding: 10px;")
        save_button.clicked.connect(self.save_partner)  # Привязываем обработчик для сохранения данных

        # Основной layout окна
        layout = QVBoxLayout()
        
        # Шапка окна с логотипом и заголовком
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #F4E8D3;")
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(logo_label)
        header_layout.addWidget(app_title)
        
        # Добавляем шапку, форму и кнопку на основной layout
        layout.addWidget(header_widget)
        layout.addLayout(form_layout)
        layout.addWidget(save_button)

        self.setLayout(layout)  # Устанавливаем layout для окна

    def save_partner(self):
        # Получаем значения из полей ввода
        name = self.name_input.text().strip()
        inn = self.inn_input.text().strip()
        director = self.director_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        # Проверка на пустые поля
        if not name:
            self.show_message("Ошибка", "Поле 'Наименование' не может быть пустым.", QMessageBox.Critical)
            return
        if not inn:
            self.show_message("Ошибка", "Поле 'ИНН' не может быть пустым.", QMessageBox.Critical)
            return
        if not director:
            self.show_message("Ошибка", "Поле 'ФИО директора' не может быть пустым.", QMessageBox.Critical)
            return
        if not phone:
            self.show_message("Ошибка", "Поле 'Телефон' не может быть пустым.", QMessageBox.Critical)
            return
        if not email:
            self.show_message("Ошибка", "Поле 'Email' не может быть пустым.", QMessageBox.Critical)
            return
        
        try:
            # Получаем выбранные значения для типа партнера и юридического адреса
            type_partner = self.session.query(Type_partner).filter_by(наименование=self.type_input.currentText()).first()
            legal_address = self.session.query(Legal_address).filter_by(город=self.address_input.currentText().split(",")[0]).first()

            # Если не выбраны тип партнера или адрес
            if not type_partner or not legal_address:
                raise ValueError("Необходимо выбрать тип партнера и юридический адрес.")

            if self.partner:
                # Если редактируем существующего партнера
                self.partner.наименование = self.name_input.text()
                self.partner.id_тип = type_partner.id
                self.partner.id_юр_адрес = legal_address.id
                self.partner.инн = self.inn_input.text()
                self.partner.фио_директора = self.director_input.text()
                self.partner.телефон = self.phone_input.text()
                self.partner.email = self.email_input.text()
                self.partner.рейтинг = str(self.rating_input.value())
            else:
                # Если создаем нового партнера
                new_partner = Partner(
                    наименование=self.name_input.text(),
                    id_тип=type_partner.id,
                    id_юр_адрес=legal_address.id,
                    инн=self.inn_input.text(),
                    фио_директора=self.director_input.text(),
                    телефон=self.phone_input.text(),
                    email=self.email_input.text(),
                    рейтинг=str(self.rating_input.value())
                )
                self.session.add(new_partner)

            # Сохраняем изменения в базе данных
            self.session.commit()

            # Отправляем сигнал, что партнер был добавлен или обновлен
            self.partner_added.emit()

            # Показываем сообщение об успешном сохранении
            self.show_message("Успех", "Партнер успешно сохранен!", QMessageBox.Information)

            # Закрываем окно после успешного сохранения
            self.accept()

        except Exception as e:
            # В случае ошибки показываем сообщение с описанием ошибки
            self.show_message("Ошибка", f"Не удалось сохранить данные: {str(e)}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        # Метод для отображения сообщений
        msg = QMessageBox()
        msg.setIcon(icon)  # Устанавливаем иконку сообщения
        msg.setText(message)  # Устанавливаем текст сообщения
        msg.setWindowTitle(title)  # Устанавливаем заголовок окна сообщения
        msg.exec()  # Отображаем сообщение