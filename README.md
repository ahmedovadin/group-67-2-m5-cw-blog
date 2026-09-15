# Blog API

REST API для блога с постами и комментариями.

## Стек

- Python 3.14
- Django 6.1
- Django REST Framework
- PostgreSQL (через Docker)
- SimpleJWT (JWT-аутентификация)
- drf-yasg (Swagger)

## Как запустить

1. **Клонировать репозиторий:**

```bash
   git clone <url>
   cd blog
```

2. **Создать виртуальное окружение:**

```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. **Установить зависимости:**

```bash
   pip install -r requirements.txt
```

4. **Создать файл `.env` в корне проекта и заполнить переменными**

5. **Запустить PostgreSQL через Docker:**

```bash
    docker run --name <your-container-name> \
    -e POSTGRES_PASSWORD=<your-pass> \
    -e POSTGRES_USER=<your-user> \
    -e POSTGRES_DB=<your-db-name> \
    -p 5432:5432 \
    -d postgres:16
```

6. **Применить миграции:**

```bash
   python manage.py migrate
```

7. **Создать суперпользователя (опционально):**

```bash
   python manage.py createsuperuser
```

8. **Запустить сервер:**

```bash
   python manage.py runserver
```

## Документация API

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Эндпоинты

### Аутентификация

- `POST /api/v1/users/registration/` — регистрация
- `POST /api/v1/users/authorization/` — авторизация, получение JWT токена

### Посты

- `GET /api/v1/posts/` — список опубликованных постов (пагинация)
- `POST /api/v1/posts/` — создать пост (требуется JWT)
- `GET /api/v1/posts/{id}/` — детальный пост
- `PUT/PATCH /api/v1/posts/{id}/` — обновить (только автор)
- `DELETE /api/v1/posts/{id}/` — удалить (только автор)

### Комментарии

- `GET /api/v1/posts/{id}/comments/` — список комментариев к посту
- `POST /api/v1/posts/{id}/comments/` — добавить комментарий (JWT)
- `PUT/PATCH /api/v1/posts/comments/{id}/` — обновить (только автор)
- `DELETE /api/v1/posts/comments/{id}/` — удалить (только автор)

## Использование JWT

1. Получи токен через `POST /api/v1/users/authorization/`
2. В защищённые запросы добавляй заголовок:

Authorization: Token <key>

## Модели

**Post:**

- author (FK на User)
- title
- body
- created_at, updated_at
- is_published

**Comment:**

- post (FK на Post)
- author (FK на User)
- body
- created_at, updated_at
- is_approved

## Права доступа

- Гости: только чтение опубликованных постов и комментариев
- Авторизованные: создание постов и комментариев
- Только автор: редактирование и удаление своих записей
