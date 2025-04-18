# Booking API

Микросервис для бронирования столиков в ресторане. Легко запускается, покрыт тестами, имеет мониторинг и логирование.

---

## 📦 Состав

- **FastAPI** — backend-приложение
- **PostgreSQL** — база данных
- **Grafana + Loki + Promtail** — логирование контейнеров
- **Pytest** — тестирование
- **Docker Compose** — оркестрация

---

## ▶️ Запуск проекта (локально)

### 1. Клонируй репозиторий

```
git clone https://github.com/shengnaan/test-task-api
cd test-task-api
```

### 2. Создай и активируй venv

```
python -m venv venv
venv\Scripts\activate
```

### 3. Подготовка `.env`

Создай файл `.env` в корне проекта с переменными окружения (какие нужны - см. env_template)

### 4. Запуск приложения

```
docker compose up --build
```

*из-за различия путей в линуксе и виндовс логирование будет работать только на винде, для линукса надо немного изменить docker compose
Документация(Swagger) будет доступна по адресу:

📌 http://localhost:8000/docs

### 5. Grafana (визуализация логов)

📌 http://localhost:3000

Логин и пароль по умолчанию: admin / admin

Чтобы посмотреть логи *приложения*:
 * Перейди в Explore
 * Как дата-сорс выбираем Loki
 * Выполняем данный запрос:

```
{container="booking_api"}
```

## Дополнительно

На Github настроено CI, для проверки линтером и прохождения всех тестов после пуша.
Но можно запустать тесты локально (в репозитории присутствует готовый .env.test для этого), через команду:
```
docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit --exit-code-from test_app
```

Также попробовать потыкать API можно тут - http://45.159.208.216:7000/docs

Grafana расположена на соответствующем порте, логин и пароль по умолчанию.
