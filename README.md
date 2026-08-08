# Тестовое задание
### Авторизация используя телеграм хаш и jwt на бэкенде

# Для начало
### Для того чтобы запустить проект нужны
 * openssl
 * docker
 * docker-compose
 * python
 * curl

### Копируем репозиторий
```shell
git clone https://github.com/sultankurb/telegram_auth_on_fastapi.git

cd telegram_auth_on_fastapi/
```

### Дальше на линуксе даем права скрипту для подготовки
```shell
chdmod +x start/*.sh
./start/start.sh
```
### Предпоследний шаг
Нужно в .env поменять API_TOKEN на токен вашего ю=бота в телеграм

### Последний шаг
```shell
cd docker
docker compose up --build
```


## Использование
### Для получения хэша как у телеграма нужно запустить файл по имени signature.py
```shell
uv run application/signarute.py
python3 application/signature.py
```
### Он выведет хэш для использования

# Примеры использования API с помощью curl

# 1. Авторизация через Telegram
# Для этого вам нужно получить данные от Telegram, включая хеш.
# Файл signature.py в проекте поможет сгенерировать тестовый хеш.
```shell
curl -X POST -H "Content-Type: application/json" \
-d '{
  "id": 123456789,
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "photo_url": "https://t.me/i/userpic/320/johndoe.jpg",
  "auth_date": 1678886400,
  "hash": "your_telegram_hash_here"
}' \
http://localhost:8000/api/auth/telegram
```
# 2. Получение информации о текущем пользователе (профиль)
# Требует JWT токена, полученного при авторизации.
# Замените <your_jwt_token> на ваш токен.
```shell
curl -X GET -H "Authorization: Bearer <your_jwt_token>" \
http://localhost:8000/api/me
```
# 3. Обновление токена доступа
# Используйте refresh_token, полученный при авторизации.
# Замените <your_refresh_token> на ваш токен.
```shell
curl -X POST \
"http://localhost:8000/api/auth/refresh?refresh_token=<your_refresh_token>"
```
# 4. Выход из системы
# Требует JWT токена, полученного при авторизации.
# Замените <your_jwt_token> на ваш токен.
```shell
curl -X POST -H "Authorization: Bearer <your_jwt_token>" \
http://localhost:8000/api/auth/logout
```
