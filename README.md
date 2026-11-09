Каждый JSON-файл имеет следующую структуру:

```json
{
    "albums": [
        {
            "title": "Abbey Road",
            "artist": "The Beatles",
            "year": 1969,
            "genre": "Rock",
            "tracks": 17
        }
    ]
}
```

## Требования

- Python 3.10+
- Django 4.x+

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/CenturyOnce/lub_json
cd lub_json
```

### 2. Создание виртуального окружения

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install django
```

### 4. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Структура проекта

```
music_albums_project/
├── manage.py                  # Точка входа Django
├── music_albums_project/      # Настройки проекта
│   ├── settings.py            # Конфигурация (включая DATA_DIR)
│   ├── urls.py                # Корневая маршрутизация
│   └── wsgi.py
├── albums/                    # Основное приложение
│   ├── forms.py               # Форма ввода альбома с валидацией
│   ├── utils.py               # Логика работы с файлами
│   ├── views.py               # Обработчики запросов
│   ├── urls.py                # Маршруты приложения
│   └── templates/albums/
│       └── home.html          # Главный шаблон
├── albums_data/               # Папка с JSON-файлами (игнорируется Git)
├── .gitignore
└── README.md
```

## Как это работает

1. **Сохранение через форму:** данные проходят валидацию Django Forms → упаковываются в JSON → записываются в новый файл с UUID-именем в папку `albums_data/`.
2. **Загрузка файла:** имя файла от пользователя игнорируется (защита от Path Traversal) → файл сохраняется под новым именем → парсится JSON → проверяется структура → при ошибке файл удаляется.
3. **Отображение:** при каждом GET-запросе сканируется папка `albums_data/`, читаются все JSON-файлы, данные агрегируются и отображаются в таблице.