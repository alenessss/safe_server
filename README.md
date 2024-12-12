Это приложение на Flask предоставляет функциональность для добавления пользователей в базу данных и отображения их списка. Приложение использует безопасные методы для защиты от SQL-инъекций и XSS уязвимостей.

## Особенности

- Безопасное добавление пользователей в базу данных с использованием SQLAlchemy ORM, предотвращающее SQL инъекции.
- Защищенный вывод данных с экранированием для предотвращения XSS атак.

## Установка и запуск

1. Клонируйте репозиторий на ваш локальный компьютер:

   ```bash
   git clone git@github.com:alenessss/safe_server.git
   cd safe_server

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv

4. Активируйте виртуальное окружение:

На Windows:
```bash
venv\Scripts\activate

На MacOS/Linux:
```bash
source venv/bin/activate
