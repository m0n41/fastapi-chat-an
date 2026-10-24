# Анонимный чат

Небольшой чат на FastAPI с обменом сообщениями через WebSocket. Интерфейс адаптирован для компьютеров и мобильных устройств.

## Требования

- Python 3.10 или новее
- pip

## Установка и запуск

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Использование

1. Введите имя длиной от 2 до 30 символов и войдите в чат.
2. Отправляйте сообщения длиной до 1000 символов.
3. Нажмите Enter для отправки или Shift+Enter для новой строки.

## Структура

- `app/main.py` — создание FastAPI-приложения и главная страница.
- `app/chat/router.py` — WebSocket-обработчик чата.
- `app/chat/connection_manager.py` — управление соединениями и рассылка сообщений.
- `app/static/index.html` — интерфейс чата.
- `app/config.py` — модель настроек для конфигурации приложения.

## Примечания

- Список подключённых пользователей хранится в памяти процесса: при перезапуске сервера соединения сбрасываются.
- Для текущего локального чата база данных и файл `.env` не требуются.
- Не добавляйте в Git виртуальное окружение, пароли, токены и другие секреты.
