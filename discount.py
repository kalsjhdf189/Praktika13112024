from datebase import Partner, history_implementation

def get_total_sales(partner_id, session):
    # Запрос к базе данных для подсчета всех продаж данного партнера
    sales = session.query(history_implementation).filter(history_implementation.c.id_партнер == partner_id).all()
    total_sales = sum(int(sale.количество) for sale in sales)  # Предполагаем, что 'количество' - это количество реализованных товаров
    return total_sales

def calculate_discount(total_sales):
    # Логика расчета скидки в зависимости от объема продаж
    if total_sales < 10000:
        return 0
    elif 10000 <= total_sales < 50000:
        return 5
    elif 50000 <= total_sales < 300000:
        return 10
    else:
        return 15