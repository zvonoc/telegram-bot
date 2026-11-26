from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Выбор языка, стартовое меню
def language_selection_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="Русский", callback_data='get_person')],
        [InlineKeyboardButton(text="English", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

# Тарифные планы
def tariff_plans():
    inline_kb_list = [
        [InlineKeyboardButton(text="Неделя", callback_data='get_person')],
        [InlineKeyboardButton(text="Месяц", callback_data='back_home')],
        [InlineKeyboardButton(text="3 Месяца", callback_data='back_home')],
        [InlineKeyboardButton(text="6 Месяцев", callback_data='back_home')],
        [InlineKeyboardButton(text="Навсегда", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

# Оплата
def payment():
    inline_kb_list = [
        [InlineKeyboardButton(text="Оплатить", callback_data='get_person')],
        [InlineKeyboardButton(text="<- Назад", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

# Меню после оплаты
def rest_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="<- Назад", callback_data='get_person')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)