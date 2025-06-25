# Проект API для Yatube Final

REST API для социальной сети Yatube, реализованное на Django REST Framework.  
API предоставляет функционал для работы с постами, комментариями, группами и подписками пользователей.

## Как развернуть проект локально

1. Клонировать репозиторий и перейти в него:

```bash
git clone https://github.com/ваш-логин/api_final_yatube.git
cd api_final_yatube
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/MacOS:
source venv/bin/activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Применить миграции:

```bash
python manage.py migrate
```

5. Создать суперпользователя:

```bash
python manage.py createsuperuser
```

6. Запустить сервер:

```bash
python manage.py runserver
```

## Аутентификация

Для работы с API необходимо получить JWT-токен:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ ^
-H "Content-Type: application/json" ^
-d '{"username":"ваш_логин", "password":"ваш_пароль"}'
```

Используйте полученный токен в заголовках запросов:
`Authorization: Bearer ваш_токен`

## Примеры запросов к API

### Работа с постами

Получение публикации:

```
GET /api/v1/posts/{id}/
```

Пример ответа (200 OK):

```
{
  "id": 1,
  "author": "username",
  "text": "Текст публикации",
  "pub_date": "2023-05-15T12:00:00Z",
  "image": null,
  "group": 1
}
```

```bash
curl -X GET http://127.0.0.1:8000/api/v1/posts/1/
```

Создание поста:

```
POST /api/v1/posts/
```

Тело запроса:

```
{
  "text": "Новый пост",
  "group": 1
}
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
-H "Authorization: Bearer ваш_токен" \
-H "Content-Type: application/json" \
-d '{"text":"Текст поста", "group":1}'
```

### Комментарии

Добавление комментария:

```
POST /api/v1/posts/{post_id}/comments/
```

Пример ответа (201 Created):

```
{
  "id": 1,
  "author": "username",
  "text": "Отличный пост!",
  "created": "2023-05-15T12:30:00Z",
  "post": 1
}
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/1/comments/ \
-H "Authorization: Bearer ваш_токен" \
-H "Content-Type: application/json" \
-d '{"text":"Мой комментарий"}'
```

### Группы

Получение информации о сообществе:

```
GET /api/v1/groups/{id}/
```

Пример ответа (200 OK):

```
{
  "id": 1,
  "title": "Название группы",
  "slug": "group-slug",
  "description": "Описание группы"
}
```

### Подписки

Получение списка подписок:

```
GET /api/v1/follow/
```

Подписка на автора:

```
POST /api/v1/follow/
```

Тело запроса:

```
{
  "following": "username_автора"
}
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/follow/ \
-H "Authorization: Bearer ваш_токен" \
-H "Content-Type: application/json" \
-d '{"following":"username"}'
```
