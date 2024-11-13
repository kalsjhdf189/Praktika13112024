from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from datebase import Partner, Connect  # Импортируем модели Partner и Connect для работы с базой данных
from PartnerForm import PartnerForm  # Импортируем форму для добавления/редактирования партнера
from ProductRequestDialog import ProductRequestDialog  # Импортируем диалог для работы с реализацией продукции
from discount import calculate_discount, get_total_sales # Импортируем методы
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Класс, представляющий карточку партнера
class PartnerCard(QFrame):
    def __init__(self, partner, type_partner, session):
        super().__init__()  # Инициализация родительского класса QFrame
        self.setFrameShape(QFrame.Box)  # Устанавливаем рамку карточки
        self.setLineWidth(1)  # Устанавливаем ширину линии рамки

        self.partner = partner  # Сохраняем информацию о партнере
        self.session = session  # Соединение с базой данных
        
        # Основной layout карточки (горизонтальный)
        layout = QHBoxLayout()

        # Левая часть карточки с информацией о партнере
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel(f"{type_partner.наименование} | {partner.наименование}"))  # Наименование партнера
        left_layout.addWidget(QLabel(f"{partner.фио_директора}"))  # ФИО директора
        left_layout.addWidget(QLabel(f"{partner.телефон}"))  # Телефон
        left_layout.addWidget(QLabel(f"Рейтинг: {partner.рейтинг}"))  # Рейтинг партнера

        # Правая часть карточки с информацией о скидке
        right_layout = QVBoxLayout()
        self.discount_label = QLabel()  # Не задаем скидку сразу
        right_layout.addWidget(self.discount_label)  # Добавляем виджет скидки в layout

        # Собираем layout: добавляем левую и правую части
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        self.setLayout(layout)  # Устанавливаем layout для текущей карточки

        self.update_discount()  # Обновляем скидку после полной инициализации карточки

    def update_discount(self):
        # Обновляем скидку на интерфейсе
        self.discount_label.setText(f"Скидка: {self.update_partner_discount()}%")
    
    def update_partner_discount(self):
        total_sales = get_total_sales(self.partner.id, self.session)  # Получаем общие продажи для партнера
        discount = calculate_discount(total_sales)  # Рассчитываем скидку
        return discount

    
# Главный класс окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса QMainWindow
        self.setWindowTitle("Мастер пол")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('icon.ico'))  # Устанавливаем иконку окна
        self.setGeometry(100, 100, 800, 600)  # Устанавливаем начальные размеры окна
        self.session = Connect.create_connection()  # Создаем соединение с базой данных
        self.init_ui()  # Инициализируем пользовательский интерфейс

    def init_ui(self):
        main_layout = QVBoxLayout()  # Основной вертикальный layout для окна

        # Создаем кнопки для добавления партнера и работы с реализацией продукции
        new_partner_button = self.create_button("Добавить партнера", self.add_partner)
        btn_sales_products = self.create_button("Реализация продукции", self.show_product_request)
        report_button = self.create_button("Сгенерировать отчет", self.generate_report)

        # Логотип и название приложения
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap('logotype.png').scaled(50, 50))  # Устанавливаем логотип
        app_title = QLabel("Мастер пол")  # Название приложения
        app_title.setStyleSheet("font-family: SegoeUI; font-size: 18px; font-weight: bold;")  # Стиль для названия

        # Верхний header с логотипом, названием и кнопками
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(logo_label)
        header_layout.addWidget(app_title)
        header_layout.addWidget(new_partner_button)
        header_layout.addWidget(btn_sales_products)
        header_layout.addWidget(report_button)
        header_widget.setStyleSheet("background-color: #F4E8D3;")  # Устанавливаем стиль фона

        # Создаем область прокрутки для списка партнеров
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Прокручиваемая область будет изменять размер
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        self.update_partner_list(scroll_layout)  # Загружаем список партнеров

        self.scroll_area.setWidget(scroll_content)  # Устанавливаем область прокрутки

        # Основной layout добавляет header и область прокрутки
        main_layout.addWidget(header_widget)
        main_layout.addWidget(self.scroll_area)

        # Устанавливаем центральный виджет для окна
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Метод для создания кнопки с заданным текстом и обработчиком
    def create_button(self, text, handler):
        button = QPushButton(text)  # Создаем кнопку
        button.setStyleSheet("font-family: SegoeUI; background-color: #67BA80; color: white; border-radius: 5px; padding: 10px;")  # Стиль кнопки
        button.clicked.connect(handler)  # Подключаем обработчик нажатия
        return button

    # Метод для отображения диалога запроса на реализацию продукции
    def show_product_request(self):
        self.close()
        
        self.dialog = ProductRequestDialog(self.session)
        self.dialog.exec_()

    # Метод для обновления списка партнеров
    def update_partner_list(self, scroll_layout):
        # Очищаем текущие карточки партнеров
        for i in reversed(range(scroll_layout.count())):
            widget = scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Удаляем старые виджеты

        # Загружаем новых партнеров из базы данных
        partners = self.session.query(Partner).all()
        for partner in partners:
            type_partner = partner.тип_партнера  # Получаем тип партнера
            card = PartnerCard(partner, type_partner, self.session)  # Создаем карточку партнера
            # Устанавливаем обработчик нажатия на карточку для редактирования
            card.mousePressEvent = lambda event, p=partner: self.edit_partner(p)
            scroll_layout.addWidget(card)  # Добавляем карточку в layout

    # Метод для добавления нового партнера
    def add_partner(self):
        form = PartnerForm()  # Создаем форму для добавления партнера
        form.partner_added.connect(self.on_partner_added)  # Подключаем сигнал, когда партнер добавлен
        form.exec()  # Показываем форму

    # Метод для редактирования существующего партнера
    def edit_partner(self, partner):
        form = PartnerForm(partner)  # Создаем форму для редактирования партнера
        form.partner_added.connect(self.on_partner_added)  # Подключаем сигнал, когда изменения сохранены
        form.exec()  # Показываем форму

    # Метод, вызываемый после добавления или редактирования партнера
    def on_partner_added(self):
        scroll_layout = self.scroll_area.widget().layout()  # Получаем layout списка партнеров
        self.update_partner_list(scroll_layout)  # Обновляем список партнеров

    def generate_report(self):
        # Путь для сохранения PDF
        file_path = "material_calculation_report.pdf"

        # Создаем объект canvas для генерации PDF
        c = canvas.Canvas(file_path, pagesize=letter)

        # Регистрируем шрифт с поддержкой кириллицы
        pdfmetrics.registerFont(TTFont('SegoeUI', 'SegoeUIRegular.ttf'))  # Укажите путь к шрифту
        c.setFont("SegoeUI", 16)  # Устанавливаем шрифт для заголовка

        # Заголовок
        title = "Отчет по количеству материала"
        
        # Вычисляем горизонтальную позицию для центра
        title_width = c.stringWidth(title, "SegoeUI", 16)
        title_x = (letter[0] - title_width) / 2  # Центрируем заголовок по горизонтали
        c.drawString(title_x, 750, title)
        
        # Устанавливаем шрифт для основного текста
        c.setFont("SegoeUI", 12)
        text = "Расчет количества материала, требуемого для производства продукции:"

        # Разбиваем текст на несколько строк, чтобы он не выходил за пределы страницы
        lines = text.split("\n")
        y_position = 700
        for line in lines:
            c.drawString(100, y_position, line)
            y_position -= 14  # Смещаем текст вниз на 14 единиц

        # Завершаем создание PDF
        c.save()

        # Показать сообщение об успешном создании отчета
        self.show_message("Успех", "Отчет успешно Создан!", QMessageBox.Information)
        
    def show_message(self, title, message, icon):
        # Метод для отображения сообщений
        msg = QMessageBox()
        msg.setIcon(icon)  # Устанавливаем иконку сообщения
        msg.setText(message)  # Устанавливаем текст сообщения
        msg.setWindowTitle(title)  # Устанавливаем заголовок окна сообщения
        msg.exec()  # Отображаем сообщение