### Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


# Описание проекта
Foodgram - проект создан для систематизации и хранения любимых рецептов и поиска новых. В проекте реализована фильтрация рецептов по требуемым группам, добавление понравившихся рецептов в избранное, следования за авторами рецептов и формирования списка покупок по выбранным рецептам.

## Инструкция для запуска приложения
Для запуска необходимо добавить SECRETS в github.workflows

- ```DOCKER_USERNAME``` - имя пользователя в hub.docker
- ```DOCKER_PASSWORD``` - пароль
- ```HOST``` - адрес сервера
- ```USER``` - пользователь
- ```SSH_KEY``` - приватный ssh ключ
- ```PASSPHRASE``` - кодовая фраза
- ```DB_ENGINE``` - django.db.backends.postgresql
- ```DB_NAME``` - postgres (по умолчанию)
- ```POSTGRES_USER``` - postgres (по умолчанию)
- ```POSTGRES_PASSWORD``` - postgres (по умолчанию)
- ```DB_HOST``` - db
- ```DB_PORT``` - 5432
- ```SECRET_KEY``` - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
- ```ALLOWED_HOSTS``` - список разрешенных адресов
- ```TELEGRAM_TO``` - id пользователя
- ```TELEGRAM_TOKEN``` - токен бота

### При первом запуске необходимо выполнить следующие команды
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git clone https://github.com/k3llar/foodgram-project-react.git
cd foodgram-project-react/infra
```

Запустить сборку и запуск контейнеров:
```
docker-compose up
```

Выполнить миграции для базы данных:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

Наполнить базу данных:
```
docker-compose exec backend python manage.py read_data_from_json fixtures
```

Подключить статические файлы:
```
docker-compose exec backend python manage.py collectstatic --no-input - для подключения статики
```


## Пользовательские роли в проекте
1. Анонимный пользователь
2. Аутентифицированный пользователь
3. Администратор

### Анонимные пользователи могут:
1. Просматривать список рецептов;
2. Просматривать отдельные рецепты;
3. Фильтровать рецепты по тегам;
4. Создавать аккаунт.

### Аутентифицированные пользователи могут:
1. Получать данные о своей учетной записи;
2. Изменять свой пароль;
3. Просматривать, публиковать, удалять и редактировать свои рецепты;
4. Добавлять понравившиеся рецепты в избранное и удалять из избранного;
5. Добавлять рецепты в список покупок и удалять из списка;
6. Подписываться и отписываться на авторов;
7. Скачать список покупок

### Набор доступных эндпоинтов 👇:
- ```api/docs/redoc``` - Подробная документация по работе API.
- ```api/tags/``` - Получение, списка тегов (GET).
- ```api/ingredients/``` - Получение, списка ингредиентов (GET).
- ```api/ingredients/``` - Получение ингредиента с соответствующим id (GET).
- ```api/tags/{id}``` - Получение, тега с соответствующим id (GET).
- ```api/recipes/``` - Получение списка с рецептами и публикация рецептов (GET, POST).
- ```api/recipes/{id}``` - Получение, изменение, удаление рецепта с соответствующим id (GET, PUT, PATCH, DELETE).
- ```api/recipes/{id}/shopping_cart/``` - Добавление рецепта с соответствующим id в список покупок и удаление из списка (GET, DELETE).
- ```api/recipes/download_shopping_cart/``` - Скачать файл со списком покупок TXT (в дальнейшем появиться поддержка PDF) (GET).
- ```api/recipes/{id}/favorite/``` - Добавление рецепта с соответствующим id в список избранного и его удаление (GET, DELETE).

#### Операции с пользователями 👇:
- ```api/users/``` - получение информации о пользователе и регистрация новых пользователей. (GET, POST).
- ```api/users/{id}/``` - Получение информации о пользователе. (GET).
- ```api/users/me/``` - получение и изменение данных своей учётной записи. Доступна любым авторизованными пользователям (GET).
- ```api/users/set_password/``` - изменение собственного пароля (PATCH).
- ```api/users/{id}/subscribe/``` - Подписаться на пользователя с соответствующим id или отписаться от него. (GET, DELETE).
- ```api/users/subscribe/subscriptions/``` - Просмотр пользователей на которых подписан текущий пользователь. (GET).

#### Аутентификация и создание новых пользователей 👇:
- ```api/auth/token/login/``` - Получение токена (POST).
- ```api/auth/token/logout/``` - Удаление токена (POST).

## Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос для регистрации нового пользователя с параметрами
***email username first_name last_name password***
на эндпойнт ```/api/users/```
2. Пользователь отправляет POST-запрос со своими регистрационными данными ***email password*** на эндпоинт ```/api/token/login/``` , в ответе на запрос ему приходит auth-token. Примечание: При взаимодействии с фронтэндом приложения операция два происходит под капотом при переходе по эндпоинту ```/api/token/login/```.
