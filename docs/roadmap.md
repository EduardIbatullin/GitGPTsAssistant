## 🚀 Дорожная карта развития проекта GitGPTsAssistant

Поэтапный план модернизации FastAPI-сервиса для интеллектуальной работы с GitHub-репозиториями.

---

### 🔰 ~~Фаза 0. Подготовка окружения и авторизация~~ ✅ *(завершена 2025‑05‑06)*
- [x] Настройка `.env`, конфигурации FastAPI и GitHub токена
- [x] Валидация токена на старте
- [x] Документация по запуску и `docs/env.example`

---

### 📁 ~~Фаза 1. Базовый CRUD для файлов~~ ✅ *(завершена 2025‑05‑06)*
- [x] `GET /repos/{repo}/structure`
- [x] `GET /repos/{repo}/file`
- [x] `POST /repos/{repo}/file`
- [x] `PUT /repos/{repo}/file`
- [x] `DELETE /repos/{repo}/file`
- [x] Тесты и документация

---

### 🔍 Фаза 2. Метаданные Git
- `GET /repos/{repo}/branches`
- `GET /repos/{repo}/commits?path=...`
- `GET /repos/{repo}/pulls`
- `GET /repos/{repo}/issues`
- Моки, тесты, примеры.

---

### 🩹 Фаза 3. Патчинг и рефакторинг
- `POST /repos/{repo}/patch`
- Интеграция с unified-diff или bsdiff
- Валидация, rollback, тесты

---

### 🧠 Фаза 4. Статический анализ
- `POST /repos/{repo}/analyze`
- `GET /repos/{repo}/analyze/report`
- flake8, bandit, radon
- JSON-отчёты, тесты

---

### 🧪 Фаза 5. Генерация тестов (GPT)
- `POST /repos/{repo}/testgen`
- `GET /repos/{repo}/tests`
- GPT-интеграция
- Тесты и авто-добавление в `tests/`

---

### 🛡️ Фаза 6. Обновление зависимостей
- `GET /repos/{repo}/deps`
- `POST /repos/{repo}/deps/update`
- PyPI, CVE-проверки, PR-патчи, тесты

---

### 🚀 Фаза 7. CI/CD и деплой
- `GET|PUT /repos/{repo}/ci-config`
- `POST /repos/{repo}/deploy`
- Генерация GitHub Actions, Dockerfile, Procfile
- Railway/Heroku CLI, dry-run тесты

---

### 📘 Фаза 8. Документация и примеры
- `GET|PUT /repos/{repo}/docs`, `POST /repos/{repo}/readme`
- OpenAPI, Postman, curl-примеры
- Проверка доступности и синтаксиса

---

### 🧠 Фаза 9. Сессии и фидбэк
- `POST /sessions`, `GET /sessions/{id}/history`, `POST /sessions/{id}/feedback`
- Сохранение истории, undo, ветвление, тесты

---

### ⏱️ Сроки реализации
- **1–2 недели**: Фазы 1–2
- **2–3 недели**: Фазы 3–4
- **3–4 недели**: Фазы 5–6
- **4–6 недель**: Фазы 7–8
- **6+ недель**: Фаза 9