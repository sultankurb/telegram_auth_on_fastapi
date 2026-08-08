#!/bin/bash

PROJECT_ROOT=$(dirname "$0")/..
CERT_DIR="$PROJECT_ROOT/application/certificates"

echo "Поиск и копирование .env.example в .env..."
find "$PROJECT_ROOT" -type f -name "*.env.example" -print0 | while IFS= read -r -d '' file; do
    cp -v "$file" "${file%.example}"
done

echo "Поиск и копирование .acl.example в .acl..."
find "$PROJECT_ROOT" -type f -name "*.acl.example" -print0 | while IFS= read -r -d '' file; do
    cp -v "$file" "${file%.example}"
done

echo "Проверка и генерация RS256 сертификатов..."
if [ ! -d "$CERT_DIR" ]; then
    echo "Создание директории для сертификатов: $CERT_DIR"
    mkdir -p "$CERT_DIR"
fi

if [ ! -f "$CERT_DIR/private.pem" ]; then
    echo "Генерация приватного ключа..."
    openssl genpkey -algorithm RSA -out "$CERT_DIR/private-key.pem" -pkeyopt rsa_keygen_bits:2048
    echo "Генерация публичного ключа..."
    openssl rsa -pubout -in "$CERT_DIR/private.pem" -out "$CERT_DIR/public-key.pem"
    echo "Сертификаты успешно созданы."
else
    echo "Сертификаты уже существуют."
fi

echo "Запуск docker-compose..."
docker compose -f "$PROJECT_ROOT/docker/docker-compose.yml" up --build -d

echo "Скрипт завершен."