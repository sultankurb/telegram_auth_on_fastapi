@echo off
REM Скрипт для копирования .env.example и .acl.example файлов, генерации сертификатов и запуска docker-compose.

set "PROJECT_ROOT=%~dp0.."
set "CERT_DIR=%PROJECT_ROOT%\application\certificates"

echo Поиск и копирование .env.example в .env...
for /r "%PROJECT_ROOT%" %%f in (*.env.example) do (
    copy /Y "%%f" "%%~dpnf"
)

echo Поиск и копирование .acl.example в .acl...
for /r "%PROJECT_ROOT%" %%f in (*.acl.example) do (
    copy /Y "%%f" "%%~dpnf"
)

echo Проверка и генерация RS256 сертификатов...
if not exist "%CERT_DIR%" (
    echo Создание директории для сертификатов: %CERT_DIR%
    mkdir "%CERT_DIR%"
)

if not exist "%CERT_DIR%\private.pem" (
    echo Генерация приватного ключа...
    openssl genpkey -algorithm RSA -out "%CERT_DIR%\private.pem" -pkeyopt rsa_keygen_bits:2048
    echo Генерация публичного ключа...
    openssl rsa -pubout -in "%CERT_DIR%\private.pem" -out "%CERT_DIR%\public.pem"
    echo Сертификаты успешно созданы.
) else (
    echo Сертификаты уже существуют.
)

echo Запуск docker-compose...
docker compose -f "%PROJECT_ROOT%\docker\docker-compose.yml" up --build -d

echo Скрипт завершен.
