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
