import logging
from decouple import config

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CopyTextButton,
    InputRichMessage,
)

logging.basicConfig(level=logging.INFO)

admin = int(config('ADMIN'))
CARD_NUMBER = config('CARD_NUMBER')

# ============================================================
# ЯЗЫКИ
# ============================================================
LANGUAGES = {
    "ru": ("🇷🇺", "Русский"),
    "uk": ("🇺🇦", "Українська"),
    "be": ("🇧🇾", "Беларуская"),
    "pl": ("🇵🇱", "Polski"),
    "cs": ("🇨🇿", "Čeština"),
    "kk": ("🇰🇿", "Қазақша"),
    "az": ("🇦🇿", "Azərbaycan"),
    "uz": ("🇺🇿", "O'zbek"),
    "tg": ("🇹🇯", "Тоҷикӣ"),
    "tr": ("🇹🇷", "Türkçe"),
    "de": ("🇩🇪", "Deutsch"),
    "fr": ("🇫🇷", "Français"),
    "it": ("🇮🇹", "Italiano"),
    "es": ("🇪🇸", "Español"),
    "pt": ("🇵🇹", "Português"),
    "ja": ("🇯🇵", "日本語"),
    "zh": ("🇨🇳", "中文"),
    "ko": ("🇰🇷", "한국어"),
}

# ============================================================
# ПЕРЕВОДЫ
# ============================================================
TRANSLATIONS = {
    "ru": {
        "choose_lang": "👇 Выберите язык:",
        "hello": "Приветствую тебя @{user} 👋",
        "choose_tariff": (
            "🛒 Выберите тариф:\n"
            "Дорогой @{user} — все тарифные планы условны, вход оплачивается любой суммой стартуя с 300 RUB, "
            "вход оплачивается один раз. Можешь задонатить любую сумму, можешь это сделать несколько раз "
            "если наша группа тебе понравиться."
        ),
        "tariffs": [
            "1 Чашка кофе | 300 RUB",
            "3 Чашки кофе | 900 RUB",
            "6 Чашек кофе | 1800 RUB",
            "10 Чашек кофе | 3000 RUB",
            "100 Чашек кофе | 30000 RUB",
        ],
        "chosen_tariff": "Ты выбрал тариф: {tariff}",
        "pay": "💳 Оплатить",
        "back": "🔙 Назад",
        "payment_method": "👋 Способ оплаты:",
        "rub": "🇷🇺 RUB",
        "final_1": (
            "Ты выбрал угостить Админа: {cups}\n"
            "Период: Навсегда"
        ),
        "final_2": (
            "Сумма к оплате: {amount}<br>"
            "Реквизиты для оплаты: Тбанк: {card}<br>"
            "После оплаты будет предоставлен доступ в наш приватный канал"
        ),
        "final_3": (
            "🚪 После успешной оплаты отправь фото, файл чека/квитанции или текст с информацией о платеже "
            "в данный чат. На чеке/квитанции должны обязательно присутствовать: дата, время и сумма платежа."
        ),
        "thanks": "Спасибо! Информация отправлена администратору ✅",
        "delivered": "Доставлено пользователю",
        "admin_reply_no_target": "Не удалось определить пользователя. Ответь (reply) на пересланное сообщение.",
    },
    "uk": {
        "choose_lang": "👇 Оберіть мову:",
        "hello": "Вітаю тебе @{user} 👋",
        "choose_tariff": (
            "🛒 Оберіть тариф:\n"
            "Дорогий @{user} — усі тарифні плани умовні, вхід оплачується будь-якою сумою починаючи з 300 RUB, "
            "вхід оплачується один раз."
        ),
        "tariffs": [
            "1 Чашка кави | 300 RUB",
            "3 Чашки кави | 900 RUB",
            "6 Чашок кави | 1800 RUB",
            "10 Чашок кави | 3000 RUB",
            "100 Чашок кави | 30000 RUB",
        ],
        "chosen_tariff": "Ти обрав тариф: {tariff}",
        "pay": "💳 Сплатити",
        "back": "🔙 Назад",
        "payment_method": "👋 Спосіб оплати:",
        "rub": "🇷🇺 RUB",
        "final_1": "Ти обрав пригостити Адміна: {cups}\nПеріод: Назавжди",
        "final_2": (
            "Сума до сплати: {amount}<br>"
            "Реквізити для оплати: Тбанк: {card}<br>"
            "Після оплати буде надано доступ до нашого приватного каналу"
        ),
        "final_3": (
            "🚪 Після успішної оплати надішли фото, файл чека/квитанції або текст з інформацією про платіж."
        ),
        "thanks": "Дякую! Інформацію надіслано адміністратору ✅",
        "delivered": "Доставлено користувачу",
        "admin_reply_no_target": "❌ Не вдалося визначити користувача. Відповідай (reply) на переслане повідомлення.",
    },
    "be": {
        "choose_lang": "👇 Выберыце мову:",
        "hello": "Вітаю цябе @{user} 👋",
        "choose_tariff": (
            "🛒 Выберыце тарыф:\n"
            "Дарагі @{user} — усе тарыфныя планы ўмоўныя, уваход аплачваецца любой сумай пачынаючы з 300 RUB, "
            "уваход аплачваецца адзін раз."
        ),
        "tariffs": [
            "1 Кубачка кавы | 300 RUB",
            "3 Кубачкі кавы | 900 RUB",
            "6 Кубачак кавы | 1800 RUB",
            "10 Кубачак кавы | 3000 RUB",
            "100 Кубачак кавы | 30000 RUB",
        ],
        "chosen_tariff": "Ты выбраў тарыф: {tariff}",
        "pay": "💳 Аплаціць",
        "back": "🔙 Назад",
        "payment_method": "👋 Спосаб аплаты:",
        "rub": "🇷🇺 RUB",
        "final_1": "Ты выбраў пачаставаць Адміна: {cups}\nПерыяд: Назаўжды",
        "final_2": (
            "Сума да аплаты: {amount}<br>"
            "Рэквізіты для аплаты: Тбанк: {card}<br>"
            "Пасля аплаты будзе дадзены доступ у наш прыватны канал"
        ),
        "final_3": (
            "🚪 Пасля паспяховай аплаты адпраў фота, файл чэка/квітанцыі або тэкст з інфармацыяй пра плацёж."
        ),
        "thanks": "Дзякуй! Інфармацыя адпраўлена адміністратару ✅",
        "delivered": "Дастаўлена карыстальніку",
        "admin_reply_no_target": "Не ўдалося вызначыць карыстальніка. Адпавядай (reply) на перасланае паведамленне.",
    },
    "pl": {
        "choose_lang": "👇 Wybierz język:",
        "hello": "Witaj @{user} 👋",
        "choose_tariff": (
            "🛒 Wybierz taryfę:\n"
            "Drogi @{user} — wszystkie plany taryfowe są umowne, wejście opłacane jest dowolną kwotą od 300 RUB, "
            "wejście opłacane jest jednorazowo."
        ),
        "tariffs": [
            "1 Filiżanka kawy | 300 RUB",
            "3 Filiżanki kawy | 900 RUB",
            "6 Filiżanek kawy | 1800 RUB",
            "10 Filiżanek kawy | 3000 RUB",
            "100 Filiżanek kawy | 30000 RUB",
        ],
        "chosen_tariff": "Wybrałeś taryfę: {tariff}",
        "pay": "💳 Zapłać",
        "back": "🔙 Wstecz",
        "payment_method": "👋 Metoda płatności:",
        "rub": "🇷🇺 RUB",
        "final_1": "Wybrałeś poczęstunek dla Admina: {cups}\nOkres: Na zawsze",
        "final_2": (
            "Kwota do zapłaty: {amount}<br>"
            "Dane do płatności: Tbank: {card}<br>"
            "Po opłaceniu zostanie udzielony dostęp do naszego prywatnego kanału"
        ),
        "final_3": (
            "🚪 Po udanej płatności wyślij zdjęcie, plik paragonu lub tekst z informacją o płatności."
        ),
        "thanks": "Dziękuję! Informacja została wysłana do administratora ✅",
        "delivered": "Dostarczono użytkownikowi",
        "admin_reply_no_target": "Nie udało się zidentyfikować użytkownika. Odpowiedz (reply) na przesłaną wiadomość.",
    },
    "cs": {
        "choose_lang": "👇 Vyberte jazyk:",
        "hello": "Vítej @{user} 👋",
        "choose_tariff": (
            "🛒 Vyberte tarif:\n"
            "Drahý @{user} — všechny tarifní plány jsou orientační, vstup se platí libovolnou částkou od 300 RUB, "
            "vstup se platí jednou."
        ),
        "tariffs": [
            "1 Šálek kávy | 300 RUB",
            "3 Šálky kávy | 900 RUB",
            "6 Šálků kávy | 1800 RUB",
            "10 Šálků kávy | 3000 RUB",
            "100 Šálků kávy | 30000 RUB",
        ],
        "chosen_tariff": "Vybral jsi tarif: {tariff}",
        "pay": "💳 Zaplatit",
        "back": "🔙 Zpět",
        "payment_method": "👋 Způsob platby:",
        "rub": "🇷🇺 RUB",
        "final_1": "Vybral jsi pohoštění pro Admina: {cups}\nObdobí: Navždy",
        "final_2": (
            "Částka k zaplacení: {amount}<br>"
            "Platební údaje: Tbank: {card}<br>"
            "Po zaplacení bude poskytnut přístup do našeho soukromého kanálu"
        ),
        "final_3": (
            "🚪 Po úspěšné platbě pošli foto, soubor účtenky nebo text s informací o platbě."
        ),
        "thanks": "Děkuji! Informace byla odeslána administrátorovi ✅",
        "delivered": "Doručeno uživateli",
        "admin_reply_no_target": "Nepodařilo se identifikovat uživatele. Odpověz (reply) na přeposlanou zprávu.",
    },
    "kk": {
        "choose_lang": "👇 Тілді таңдаңыз:",
        "hello": "Сәлеметсіз бе @{user} 👋",
        "choose_tariff": (
            "🛒 Тарифті таңдаңыз:\n"
            "Қымбатты @{user} — барлық тарифтік жоспарлар шартты, кіру 300 RUB бастап кез келген сомамен төленеді, "
            "кіру бір рет төленеді."
        ),
        "tariffs": [
            "1 Шыны кофе | 300 RUB",
            "3 Шыны кофе | 900 RUB",
            "6 Шыны кофе | 1800 RUB",
            "10 Шыны кофе | 3000 RUB",
            "100 Шыны кофе | 30000 RUB",
        ],
        "chosen_tariff": "Сіз тарифті таңдадыңыз: {tariff}",
        "pay": "💳 Төлеу",
        "back": "🔙 Артқа",
        "payment_method": "👋 Төлем әдісі:",
        "rub": "🇷🇺 RUB",
        "final_1": "Сіз Админді сыйлауды таңдадыңыз: {cups}\nКезең: Мәңгілік",
        "final_2": (
            "Төленетін сома: {amount}<br>"
            "Төлем деректері: Тбанк: {card}<br>"
            "Төлегеннен кейін жеке каналға рұқсат беріледі"
        ),
        "final_3": (
            "🚪 Сәтті төленгеннен кейін фото, чек файлын немесе төлем туралы мәтінді жіберіңіз."
        ),
        "thanks": "Рахмет! Ақпарат әкімшіге жіберілді ✅",
        "delivered": "Пайдаланушыға жеткізілді",
        "admin_reply_no_target": "Пайдаланушыны анықтау мүмкін болмады. Жіберілген хабарламаға жауап беріңіз (reply).",
    },
    "az": {
        "choose_lang": "👇 Dil seçin:",
        "hello": "Salam @{user} 👋",
        "choose_tariff": (
            "🛒 Tarif seçin:\n"
            "Əziz @{user} — bütün tarif planları şərtidir, giriş 300 RUB-dan başlayaraq istənilən məbləğlə ödənilir, "
            "giriş bir dəfə ödənilir."
        ),
        "tariffs": [
            "1 Fincan qəhvə | 300 RUB",
            "3 Fincan qəhvə | 900 RUB",
            "6 Fincan qəhvə | 1800 RUB",
            "10 Fincan qəhvə | 3000 RUB",
            "100 Fincan qəhvə | 30000 RUB",
        ],
        "chosen_tariff": "Siz tarif seçdiniz: {tariff}",
        "pay": "💳 Ödə",
        "back": "🔙 Geri",
        "payment_method": "👋 Ödəniş üsulu:",
        "rub": "🇷🇺 RUB",
        "final_1": "Siz Admini qonaq etməyi seçdiniz: {cups}\nDövr: Əbədi",
        "final_2": (
            "Ödəniləcək məbləğ: {amount}<br>"
            "Ödəniş rekvizitləri: Tbank: {card}<br>"
            "Ödənişdən sonra özəl kanalımıza giriş veriləcək"
        ),
        "final_3": (
            "🚪 Uğurlu ödənişdən sonra foto, qəbz faylı və ya ödəniş haqqında mətni göndərin."
        ),
        "thanks": "Təşəkkür! Məlumat administratora göndərildi ✅",
        "delivered": "İstifadəçiyə çatdırıldı",
        "admin_reply_no_target": "İstifadəçini müəyyən etmək mümkün olmadı. Göndərilən mesaja cavab verin (reply).",
    },
    "uz": {
        "choose_lang": "👇 Tilni tanlang:",
        "hello": "Salom @{user} 👋",
        "choose_tariff": (
            "🛒 Tarifni tanlang:\n"
            "Hurmatli @{user} — barcha tarif rejalari shartli, kirish 300 RUB dan boshlab istalgan summa bilan to'lanadi, "
            "kirish bir marta to'lanadi."
        ),
        "tariffs": [
            "1 Piyola qahva | 300 RUB",
            "3 Piyola qahva | 900 RUB",
            "6 Piyola qahva | 1800 RUB",
            "10 Piyola qahva | 3000 RUB",
            "100 Piyola qahva | 30000 RUB",
        ],
        "chosen_tariff": "Siz tarifni tanladingiz: {tariff}",
        "pay": "💳 To'lash",
        "back": "🔙 Orqaga",
        "payment_method": "👋 To'lov usuli:",
        "rub": "🇷🇺 RUB",
        "final_1": "Siz Adminni mehmon qilishni tanladingiz: {cups}\nDavr: Abadiy",
        "final_2": (
            "To'lanadigan summa: {amount}<br>"
            "To'lov rekvizitlari: Tbank: {card}<br>"
            "To'lovdan so'ng shaxsiy kanalimizga kirish beriladi"
        ),
        "final_3": (
            "🚪 Muvaffaqiyatli to'lovdan so'ng foto, chek fayli yoki to'lov haqida matn yuboring."
        ),
        "thanks": "Rahmat! Ma'lumot administratorga yuborildi ✅",
        "delivered": "Foydalanuvchiga yetkazildi",
        "admin_reply_no_target": "Foydalanuvchini aniqlab bo'lmadi. Yuborilgan xabarga javob bering (reply).",
    },
    "tg": {
        "choose_lang": "👇 Забонро интихоб кунед:",
        "hello": "Салом @{user} 👋",
        "choose_tariff": (
            "🛒 Тарифро интихоб кунед:\n"
            "Гароми @{user} — ҳамаи нақшаҳои тарифӣ шартӣ мебошанд, вуруд бо ҳама гуна маблағ аз 300 RUB пардохт мешавад, "
            "вуруд як маротиба пардохт мешавад."
        ),
        "tariffs": [
            "1 Пиёла қаҳва | 300 RUB",
            "3 Пиёла қаҳва | 900 RUB",
            "6 Пиёла қаҳва | 1800 RUB",
            "10 Пиёла қаҳва | 3000 RUB",
            "100 Пиёла қаҳва | 30000 RUB",
        ],
        "chosen_tariff": "Шумо тарифро интихоб кардед: {tariff}",
        "pay": "💳 Пардохт",
        "back": "🔙 Бозгашт",
        "payment_method": "👋 Тарзи пардохт:",
        "rub": "🇷🇺 RUB",
        "final_1": "Шумо Админро зиёфат карданро интихоб кардед: {cups}\nДавра: Ҳамеша",
        "final_2": (
            "Маблағи пардохт: {amount}<br>"
            "Реквизитҳо барои пардохт: Тбанк: {card}<br>"
            "Пас аз пардохт ба канали хусусии мо дастрасӣ дода мешавад"
        ),
        "final_3": (
            "🚪 Пас аз пардохти муваффақ фото, файли чек ё матни иттилоотро фиристед."
        ),
        "thanks": "Ташаккур! Иттилоот ба администратор фиристода шуд ✅",
        "delivered": "Ба корбар расонида шуд",
        "admin_reply_no_target": "Корбарро муайян карда нашуд. Ба паёми фиристода ҷавоб диҳед (reply).",
    },
    "tr": {
        "choose_lang": "👇 Dil seçin:",
        "hello": "Merhaba @{user} 👋",
        "choose_tariff": (
            "🛒 Tarife seçin:\n"
            "Sevgili @{user} — tüm tarife planları koşulludur, giriş 300 RUB'dan başlayan herhangi bir miktarla ödenir, "
            "giriş bir kez ödenir."
        ),
        "tariffs": [
            "1 Fincan kahve | 300 RUB",
            "3 Fincan kahve | 900 RUB",
            "6 Fincan kahve | 1800 RUB",
            "10 Fincan kahve | 3000 RUB",
            "100 Fincan kahve | 30000 RUB",
        ],
        "chosen_tariff": "Tarifini seçtin: {tariff}",
        "pay": "💳 Öde",
        "back": "🔙 Geri",
        "payment_method": "👋 Ödeme yöntemi:",
        "rub": "🇷🇺 RUB",
        "final_1": "Admini ağırlamayı seçtin: {cups}\nSüre: Sonsuza kadar",
        "final_2": (
            "Ödenecek tutar: {amount}<br>"
            "Ödeme bilgileri: Tbank: {card}<br>"
            "Ödemeden sonra özel kanalımıza erişim verilecektir"
        ),
        "final_3": (
            "🚪 Başarılı ödemeden sonra fotoğraf, makbuz dosyası veya ödeme bilgisi içeren metin gönderin."
        ),
        "thanks": "Teşekkürler! Bilgi yöneticiye gönderildi ✅",
        "delivered": "Kullanıcıya iletildi",
        "admin_reply_no_target": "Kullanıcı belirlenemedi. Gönderilen mesaja yanıt verin (reply).",
    },
    "de": {
        "choose_lang": "👇 Sprache wählen:",
        "hello": "Hallo @{user} 👋",
        "choose_tariff": (
            "🛒 Tarif wählen:\n"
            "Lieber @{user} — alle Tarifpläne sind bedingt, der Eintritt wird mit einem beliebigen Betrag ab 300 RUB bezahlt, "
            "der Eintritt wird einmalig bezahlt."
        ),
        "tariffs": [
            "1 Tasse Kaffee | 300 RUB",
            "3 Tassen Kaffee | 900 RUB",
            "6 Tassen Kaffee | 1800 RUB",
            "10 Tassen Kaffee | 3000 RUB",
            "100 Tassen Kaffee | 30000 RUB",
        ],
        "chosen_tariff": "Du hast den Tarif gewählt: {tariff}",
        "pay": "💳 Bezahlen",
        "back": "🔙 Zurück",
        "payment_method": "👋 Zahlungsmethode:",
        "rub": "🇷🇺 RUB",
        "final_1": "Du hast beschlossen, den Admin zu bewirten: {cups}\nZeitraum: Für immer",
        "final_2": (
            "Zu zahlender Betrag: {amount}<br>"
            "Zahlungsdetails: Tbank: {card}<br>"
            "Nach der Zahlung wird der Zugang zu unserem privaten Kanal gewährt"
        ),
        "final_3": (
            "🚪 Nach erfolgreicher Zahlung sende ein Foto, eine Quittungsdatei oder einen Text mit Zahlungsinformationen."
        ),
        "thanks": "Danke! Die Information wurde an den Administrator gesendet ✅",
        "delivered": "An Benutzer zugestellt",
        "admin_reply_no_target": "Benutzer konnte nicht ermittelt werden. Antworte (reply) auf die weitergeleitete Nachricht.",
    },
    "fr": {
        "choose_lang": "👇 Choisissez la langue :",
        "hello": "Salut @{user} 👋",
        "choose_tariff": (
            "🛒 Choisissez un tarif :\n"
            "Cher @{user} — tous les plans tarifaires sont conditionnels, l'entrée est payée par n'importe quel montant "
            "à partir de 300 RUB, l'entrée est payée une fois."
        ),
        "tariffs": [
            "1 Tasse de café | 300 RUB",
            "3 Tasses de café | 900 RUB",
            "6 Tasses de café | 1800 RUB",
            "10 Tasses de café | 3000 RUB",
            "100 Tasses de café | 30000 RUB",
        ],
        "chosen_tariff": "Tu as choisi le tarif : {tariff}",
        "pay": "💳 Payer",
        "back": "🔙 Retour",
        "payment_method": "👋 Méthode de paiement :",
        "rub": "🇷🇺 RUB",
        "final_1": "Tu as choisi d'offrir à l'Admin : {cups}\nPériode : Pour toujours",
        "final_2": (
            "Montant à payer : {amount}<br>"
            "Coordonnées de paiement : Tbank : {card}<br>"
            "Après le paiement, l'accès à notre canal privé sera accordé"
        ),
        "final_3": (
            "🚪 Après un paiement réussi, envoie une photo, un fichier de reçu ou un texte avec les informations de paiement."
        ),
        "thanks": "Merci ! L'information a été envoyée à l'administrateur ✅",
        "delivered": "Livré à l'utilisateur",
        "admin_reply_no_target": "Impossible d'identifier l'utilisateur. Réponds (reply) au message transféré.",
    },
    "it": {
        "choose_lang": "👇 Scegli la lingua:",
        "hello": "Ciao @{user} 👋",
        "choose_tariff": (
            "🛒 Scegli un piano:\n"
            "Caro @{user} — tutti i piani tariffari sono condizionali, l'ingresso si paga con qualsiasi importo "
            "a partire da 300 RUB, l'ingresso si paga una volta."
        ),
        "tariffs": [
            "1 Tazza di caffè | 300 RUB",
            "3 Tazze di caffè | 900 RUB",
            "6 Tazze di caffè | 1800 RUB",
            "10 Tazze di caffè | 3000 RUB",
            "100 Tazze di caffè | 30000 RUB",
        ],
        "chosen_tariff": "Hai scelto il piano: {tariff}",
        "pay": "💳 Paga",
        "back": "🔙 Indietro",
        "payment_method": "👋 Metodo di pagamento:",
        "rub": "🇷🇺 RUB",
        "final_1": "Hai scelto di offrire all'Admin: {cups}\nPeriodo: Per sempre",
        "final_2": (
            "Importo da pagare: {amount}<br>"
            "Dettagli di pagamento: Tbank: {card}<br>"
            "Dopo il pagamento verrà concesso l'accesso al nostro canale privato"
        ),
        "final_3": (
            "🚪 Dopo un pagamento riuscito invia una foto, un file di ricevuta o un testo con le informazioni di pagamento."
        ),
        "thanks": "Grazie! Le informazioni sono state inviate all'amministratore ✅",
        "delivered": "Consegnato all'utente",
        "admin_reply_no_target": "Impossibile identificare l'utente. Rispondi (reply) al messaggio inoltrato.",
    },
    "es": {
        "choose_lang": "👇 Elige el idioma:",
        "hello": "Hola @{user} 👋",
        "choose_tariff": (
            "🛒 Elige un plan:\n"
            "Estimado @{user} — todos los planes tarifarios son condicionales, la entrada se paga con cualquier importe "
            "a partir de 300 RUB, la entrada se paga una vez."
        ),
        "tariffs": [
            "1 Taza de café | 300 RUB",
            "3 Tazas de café | 900 RUB",
            "6 Tazas de café | 1800 RUB",
            "10 Tazas de café | 3000 RUB",
            "100 Tazas de café | 30000 RUB",
        ],
        "chosen_tariff": "Has elegido el plan: {tariff}",
        "pay": "💳 Pagar",
        "back": "🔙 Atrás",
        "payment_method": "👋 Método de pago:",
        "rub": "🇷🇺 RUB",
        "final_1": "Has elegido invitar al Admin: {cups}\nPeríodo: Para siempre",
        "final_2": (
            "Importe a pagar: {amount}<br>"
            "Datos de pago: Tbank: {card}<br>"
            "Después del pago se otorgará acceso a nuestro canal privado"
        ),
        "final_3": (
            "🚪 Después de un pago exitoso, envía una foto, un archivo de recibo o un texto con la información del pago."
        ),
        "thanks": "¡Gracias! La información ha sido enviada al administrador ✅",
        "delivered": "Entregado al usuario",
        "admin_reply_no_target": "No se pudo identificar al usuario. Responde (reply) al mensaje reenviado.",
    },
    "pt": {
        "choose_lang": "👇 Escolha o idioma:",
        "hello": "Olá @{user} 👋",
        "choose_tariff": (
            "🛒 Escolha um plano:\n"
            "Caro @{user} — todos os planos tarifários são condicionais, a entrada é paga com qualquer valor "
            "a partir de 300 RUB, a entrada é paga uma vez."
        ),
        "tariffs": [
            "1 Xícara de café | 300 RUB",
            "3 Xícaras de café | 900 RUB",
            "6 Xícaras de café | 1800 RUB",
            "10 Xícaras de café | 3000 RUB",
            "100 Xícaras de café | 30000 RUB",
        ],
        "chosen_tariff": "Você escolheu o plano: {tariff}",
        "pay": "💳 Pagar",
        "back": "🔙 Voltar",
        "payment_method": "👋 Método de pagamento:",
        "rub": "🇷🇺 RUB",
        "final_1": "Você escolheu presentear o Admin: {cups}\nPeríodo: Para sempre",
        "final_2": (
            "Valor a pagar: {amount}<br>"
            "Dados de pagamento: Tbank: {card}<br>"
            "Após o pagamento, será concedido acesso ao nosso canal privado"
        ),
        "final_3": (
            "🚪 Após o pagamento bem-sucedido, envie uma foto, arquivo de recibo ou texto com informações de pagamento."
        ),
        "thanks": "Obrigado! A informação foi enviada ao administrador ✅",
        "delivered": "Entregue ao usuário",
        "admin_reply_no_target": "Não foi possível identificar o usuário. Responda (reply) à mensagem encaminhada.",
    },
    "ja": {
        "choose_lang": "👇 言語を選択してください:",
        "hello": "こんにちは @{user} 👋",
        "choose_tariff": (
            "🛒 プランを選択してください:\n"
            "親愛なる @{user} — すべてのプランは条件付きです。参加費は300 RUB以上の任意の金額でお支払いいただけます。"
            "参加費は一度だけお支払いください。"
        ),
        "tariffs": [
            "コーヒー1杯 | 300 RUB",
            "コーヒー3杯 | 900 RUB",
            "コーヒー6杯 | 1800 RUB",
            "コーヒー10杯 | 3000 RUB",
            "コーヒー100杯 | 30000 RUB",
        ],
        "chosen_tariff": "あなたはプランを選択しました: {tariff}",
        "pay": "💳 支払う",
        "back": "🔙 戻る",
        "payment_method": "👋 支払い方法:",
        "rub": "🇷🇺 RUB",
        "final_1": "あなたは管理者をごちそうすることを選びました: {cups}\n期間: 永久",
        "final_2": (
            "支払金額: {amount}<br>"
            "お支払い情報: Tbank: {card}<br>"
            "お支払い後、プライベートチャンネルへのアクセスが提供されます"
        ),
        "final_3": (
            "🚪 お支払い成功後、写真、領収書ファイル、または支払い情報を含むテキストを送信してください。"
        ),
        "thanks": "ありがとうございます！情報が管理者に送信されました ✅",
        "delivered": "ユーザーに配信されました",
        "admin_reply_no_target": "ユーザーを特定できませんでした。転送されたメッセージに返信（reply）してください。",
    },
    "zh": {
        "choose_lang": "👇 请选择语言:",
        "hello": "你好 @{user} 👋",
        "choose_tariff": (
            "🛒 请选择套餐:\n"
            "亲爱的 @{user} — 所有套餐均为示意，入场费从300 RUB起任意金额支付，入场费仅需支付一次。"
        ),
        "tariffs": [
            "1杯咖啡 | 300 RUB",
            "3杯咖啡 | 900 RUB",
            "6杯咖啡 | 1800 RUB",
            "10杯咖啡 | 3000 RUB",
            "100杯咖啡 | 30000 RUB",
        ],
        "chosen_tariff": "你选择了套餐: {tariff}",
        "pay": "💳 支付",
        "back": "🔙 返回",
        "payment_method": "👋 支付方式:",
        "rub": "🇷🇺 RUB",
        "final_1": "你选择请管理员喝咖啡: {cups}\n期限: 永久",
        "final_2": (
            "应付金额: {amount}<br>"
            "付款信息: Tbank: {card}<br>"
            "付款后将获得我们私密频道的访问权限"
        ),
        "final_3": (
            "🚪 付款成功后，请将照片、收据文件或付款信息文本发送到此聊天。"
        ),
        "thanks": "谢谢！信息已发送给管理员 ✅",
        "delivered": "已送达用户",
        "admin_reply_no_target": "无法识别用户。请回复（reply）转发的消息。",
    },
    "ko": {
        "choose_lang": "👇 언어를 선택하세요:",
        "hello": "안녕하세요 @{user} 👋",
        "choose_tariff": (
            "🛒 요금제를 선택하세요:\n"
            "친애하는 @{user} — 모든 요금제는 조건부이며, 입장료는 300 RUB부터 임의의 금액으로 지불됩니다. "
            "입장료는 한 번만 지불됩니다."
        ),
        "tariffs": [
            "커피 1잔 | 300 RUB",
            "커피 3잔 | 900 RUB",
            "커피 6잔 | 1800 RUB",
            "커피 10잔 | 3000 RUB",
            "커피 100잔 | 30000 RUB",
        ],
        "chosen_tariff": "선택한 요금제: {tariff}",
        "pay": "💳 결제",
        "back": "🔙 뒤로",
        "payment_method": "👋 결제 방법:",
        "rub": "🇷🇺 RUB",
        "final_1": "관리자에게 대접하기로 선택했습니다: {cups}\n기간: 영구",
        "final_2": (
            "결제 금액: {amount}<br>"
            "결제 정보: Tbank: {card}<br>"
            "결제 후 비공개 채널에 대한 액세스가 제공됩니다"
        ),
        "final_3": (
            "🚪 결제 성공 후 사진, 영수증 파일 또는 결제 정보 텍스트를 보내주세요."
        ),
        "thanks": "감사합니다! 정보가 관리자에게 전송되었습니다 ✅",
        "delivered": "사용자에게 전달되었습니다",
        "admin_reply_no_target": "사용자를 식별할 수 없습니다. 전달된 메시지에 답장(reply)하세요.",
    },
}

# ============================================================
# FSM
# ============================================================
class Form(StatesGroup):
    choosing_lang = State()
    choosing_tariff = State()
    confirm = State()
    payment_method = State()
    final = State()

# ============================================================
# РОУТЕР
# ============================================================
router = Router()

admin_msg_to_user: dict[int, int] = {}
user_langs: dict[int, str] = {}


def t(lang: str, key: str, **kwargs):
    val = TRANSLATIONS.get(lang, TRANSLATIONS["ru"])[key]
    if isinstance(val, str):
        return val.format(**kwargs) if kwargs else val
    return val


def rich_html(text: str) -> InputRichMessage:
    """Обёртка: собирает InputRichMessage из HTML-строки."""
    return InputRichMessage(html=text)


async def safe_edit_rich(message: Message, rich_message: InputRichMessage, reply_markup=None):
    """Редактирует сообщение, заменяя его на Rich Message. Если нельзя — удаляет и отправляет новое."""
    try:
        await message.edit_text(rich_message=rich_message, reply_markup=reply_markup)
    except TelegramBadRequest:
        try:
            await message.delete()
        except TelegramBadRequest:
            pass
        await message.answer_rich(rich_message=rich_message, reply_markup=reply_markup)


def get_user(cb: CallbackQuery) -> str:
    return cb.from_user.username or cb.from_user.first_name or "друг"


def tariff_kb(lang: str) -> InlineKeyboardMarkup:
    tariffs_list = t(lang, "tariffs")
    buttons = []
    for i, tariff in enumerate(tariffs_list):
        buttons.append([InlineKeyboardButton(text=tariff, callback_data=f"tariff:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ---------- /start (Rich Message) ----------
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.choosing_lang)

    buttons = []
    row = []
    for code, (flag, name) in LANGUAGES.items():
        row.append(InlineKeyboardButton(text=f"{flag} {name}", callback_data=f"lang:{code}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer_rich(
        rich_message=rich_html(t("ru", "choose_lang")),
        reply_markup=kb,
    )


# ---------- ШАГ 2: выбор языка → приветствие + тарифы (Rich, на месте) ----------
@router.callback_query(F.data.startswith("lang:"))
async def choose_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data.split(":")[1]
    await state.update_data(lang=lang)
    await state.set_state(Form.choosing_tariff)
    user = get_user(cb)

    user_langs[cb.from_user.id] = lang

    text = t(lang, "hello", user=user) + "<br><br>" + t(lang, "choose_tariff", user=user)
    await safe_edit_rich(cb.message, rich_html(text), reply_markup=tariff_kb(lang))
    await cb.answer()


# ---------- ШАГ 3: выбор тарифа → подтверждение (Rich, на месте) ----------
@router.callback_query(F.data.startswith("tariff:"))
async def choose_tariff(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    idx = int(cb.data.split(":")[1])
    tariffs = t(lang, "tariffs")
    tariff = tariffs[idx]
    await state.update_data(tariff=tariff, tariff_idx=idx)
    await state.set_state(Form.confirm)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "pay"), callback_data="pay")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_tariff")],
    ])
    await safe_edit_rich(cb.message, rich_html(t(lang, "chosen_tariff", tariff=tariff)), reply_markup=kb)
    await cb.answer()


# ---------- Назад на шаг 2 (Rich, на месте) ----------
@router.callback_query(F.data == "back_to_tariff")
async def back_to_tariff(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Form.choosing_tariff)
    user = get_user(cb)

    text = t(lang, "hello", user=user) + "<br><br>" + t(lang, "choose_tariff", user=user)
    await safe_edit_rich(cb.message, rich_html(text), reply_markup=tariff_kb(lang))
    await cb.answer()


# ---------- ШАГ 4: оплатить → способ оплаты (Rich, на месте) ----------
@router.callback_query(F.data == "pay")
async def pay(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Form.payment_method)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "rub"), callback_data="method:rub")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_confirm")],
    ])
    await safe_edit_rich(cb.message, rich_html(t(lang, "payment_method")), reply_markup=kb)
    await cb.answer()


# ---------- Назад на шаг 3 (Rich, на месте) ----------
@router.callback_query(F.data == "back_to_confirm")
async def back_to_confirm(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    tariff = data.get("tariff", "")
    await state.set_state(Form.confirm)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "pay"), callback_data="pay")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_tariff")],
    ])
    await safe_edit_rich(cb.message, rich_html(t(lang, "chosen_tariff", tariff=tariff)), reply_markup=kb)
    await cb.answer()


# ---------- ШАГ 5: выбор RUB → одно Rich Message (на месте) ----------
@router.callback_query(F.data == "method:rub")
async def method_rub(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    tariff = data.get("tariff", "")
    await state.set_state(Form.final)

    cups = tariff.split("|")[0].strip()
    amount = tariff.split("|")[1].strip() if "|" in tariff else tariff

    text = (
        t(lang, "final_1", cups=cups) + "<br><br>" +
        t(lang, "final_2", amount=amount, card=CARD_NUMBER) + "<br><br>" +
        t(lang, "final_3")
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_method")],
    ])
    await safe_edit_rich(cb.message, rich_html(text), reply_markup=kb)
    await cb.answer()


# ---------- Назад на шаг 4 (Rich, на месте) ----------
@router.callback_query(F.data == "back_to_method")
async def back_to_method(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(Form.payment_method)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "rub"), callback_data="method:rub")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_confirm")],
    ])
    await safe_edit_rich(cb.message, rich_html(t(lang, "payment_method")), reply_markup=kb)
    await cb.answer()


# ============================================================
# ОТВЕТ АДМИНА ПОЛЬЗОВАТЕЛЮ (без изменений)
# ============================================================
@router.message(F.from_user.id == admin, F.reply_to_message)
async def admin_reply_to_user(message: Message):
    replied_id = message.reply_to_message.message_id
    target_user_id = admin_msg_to_user.get(replied_id)

    if not target_user_id:
        await message.reply(t("ru", "admin_reply_no_target"))
        return

    lang = user_langs.get(target_user_id, "ru")

    try:
        await message.copy_to(chat_id=target_user_id)
        await message.reply(t(lang, "delivered"))
    except Exception as e:
        logging.exception("Admin reply failed: %s", e)
        await message.reply(f"❌ Не удалось отправить пользователю: {e}")


# ============================================================
# ПЕРЕСЫЛКА АДМИНУ (без изменений)
# ============================================================
@router.message(F.photo | F.document | F.video | F.animation | F.text)
async def forward_to_admin(message: Message, state: FSMContext):
    try:
        sent = await message.forward(admin)
        admin_msg_to_user[sent.message_id] = message.from_user.id

        data = await state.get_data()
        lang = data.get("lang", "ru")
        user_langs[message.from_user.id] = lang

        await message.reply(t(lang, "thanks"))
    except Exception as e:
        logging.exception("Forward to admin failed: %s", e)
        await message.reply("Не удалось отправить администратору ❌")