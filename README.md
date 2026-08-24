# Домашние задания по Django

Этот репозиторий содержит мой проект для выполнения домашних заданий по курсу Python/Django.

## Стек технологий

- Python
- Django
- SQLite3

## Как запустить проект локально

1. Склонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv`
   `source venv/Scripts/activate` (для Git Bash)
3. Установите зависимости:
   `pip install -r requirements.txt`
4. Примените миграции базы данных:
   `python manage.py migrate`
5. Запустите локальный сервер:
   `python manage.py runserver`
