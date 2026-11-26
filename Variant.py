from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router

router = Router()

# ---------- Словари для локализации и тарифов ----------
TEXTS = {
    "ru": {"welcome": "Выберите язык:", "step2": "Выберите тариф:", "step3": "Настройки тарифа:",
           "step4": "Доп. опции:", "step5": "Подтвердите:"},
    "en": {"welcome": "Choose language:", "step2": "Choose plan:", "step3": "Plan settings:",
           "step4": "Extra options:", "step5": "Confirm:"},
}
PLANS = {
    "ru": {"basic": "Базовый", "pro": "Профи"},
    "en": {"basic": "Basic", "pro": "Pro"},
}

# ---------- Хелпер: строим клавиатуру по шагу и контексту ----------
def build_kb(step: int, lang: str, plan: str):
    kb = InlineKeyboardBuilder()
    if step == 1:  # выбор языка
        kb.button(text="🇷🇺 Русский", callback_data="step2:ru:none")
        kb.button(text="🇬🇧 English", callback_data="step2:en:none")
    elif step == 2:  # выбор тарифа (зависит от языка)
        for key, name in PLANS[lang].items():
            kb.button(text=name, callback_data=f"step3:{lang}:{key}")
        kb.button(text="⬅️ Назад", callback_data="step1:none:none")
    elif step == 3:  # настройки тарифа (зависит от языка и тарифа)
        # например, для pro добавляем доп. кнопку
        kb.button(text="Скорость", callback_data=f"step4:{lang}:{plan}:speed")
        kb.button(text="Качество", callback_data=f"step4:{lang}:{plan}:quality")
        if plan == "pro":
            kb.button(text="Премиум-опция", callback_data=f"step4:{lang}:{plan}:premium")
        kb.button(text="⬅️ Назад", callback_data=f"step2:{lang}:none")
    elif step == 4:
        kb.button(text="Да, продолжить", callback_data=f"step5:{lang}:{plan}")
        kb.button(text="⬅️ Назад", callback_data=f"step3:{lang}:{plan}")
    elif step == 5:
        kb.button(text="✅ Подтвердить", callback_data=f"done:{lang}:{plan}")
        kb.button(text="⬅️ Назад", callback_data=f"step4:{lang}:{plan}")
    kb.adjust(2)
    return kb.as_markup()

# ---------- Старт ----------
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(TEXTS["ru"]["welcome"], reply_markup=build_kb(1, "ru", "none"))

# ---------- Универсальный обработчик шагов ----------
@router.callback_query(F.data.startswith(("step", "done")))
async def handle_step(call: CallbackQuery):
    parts = call.data.split(":")
    step_action = parts[0]
    lang = parts[1] if len(parts) > 1 else "ru"
    plan = parts[2] if len(parts) > 2 else "none"
    extra = parts[3] if len(parts) > 3 else None  # для шага 3 -> 4

    if step_action == "done":
        await call.message.edit_text(
            f"Готово! Язык: {lang}, тариф: {plan}. Спасибо!")
        await call.answer()
        return

    step_num = int(step_action.replace("step", ""))
    # Если перешли с шага 3 по конкретной опции — можно учесть extra
    text = TEXTS[lang].get(f"step{step_num}", "Меню")

    await call.message.edit_text(text, reply_markup=build_kb(step_num, lang, plan))
    await call.answer()