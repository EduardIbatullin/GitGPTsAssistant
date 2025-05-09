# GitHub Repo Assistant API

Лёгкий FastAPI-сервер для работы с вашими репозиториями на GitHub.  
Позволяет:
- Просмотреть структуру репозитория  
- Получить содержимое файла  
- Создать, обновить и удалить файл  
- Получить метаданные Git (ветки, коммиты, PR, issues)  
- Генерировать патчи, тесты, документацию, CI/CD  
- Анализировать код и управлять зависимостями  

---

## 🧭 Дорожная карта

Полный план расширения API описан в файле [`docs/roadmap.md`](./docs/roadmap.md) (создаётся позже). Кратко:

1. CRUD-файлы
2. Git-метаданные (ветки, коммиты, PR)
3. Патчинг и рефакторинг
4. Статический анализ
5. Генерация тестов
6. Обновление зависимостей
7. Авто-CI/CD
8. Документация и примеры
9. Сессии и фидбэк

---

## 📋 Пререквизиты

- Python 3.8+  
- GitHub Personal Access Token с правами `repo`  
- Зависимости (см. `requirements.txt` и `requirements-dev.txt`)  

---

## 🚀 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/your-project.git
   cd your-project
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # Linux/macOS
   .venv\Scripts\activate          # Windows
   ```

3. Установите основные зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. (Опционально) Установите dev-зависимости:
   ```bash
   pip install -r requirements-dev.txt
   ```

---

## 🔧 Конфигурация

1. Создайте файл `.env` в корне проекта:
   ```dotenv
   MY_GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
   MY_GITHUB_USERNAME=your-github-username
   ```

2. Убедитесь, что `app/core/config.py` читает эти переменные.

---

## ▶️ Запуск сервера

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📮 Примеры эндпоинтов

### Получить структуру репозитория
```
GET /repos/{repo}/structure
```

### Получить содержимое файла
```
GET /repos/{repo}/file?path={path}
```

### Создать файл
```
POST /repos/{repo}/file
```

### Обновить файл
```
PUT /repos/{repo}/file
```

### Удалить файл
```
DELETE /repos/{repo}/file
```

### Получить список веток
```
GET /repos/{repo}/branches
```

### Получить список коммитов
```
GET /repos/{repo}/commits?path=src/main.py
```

### Получить список Pull Requests
```
GET /repos/{repo}/pulls
```

### Получить список Issues
```
GET /repos/{repo}/issues
```

(Подробнее — см. Swagger или `test_requests.http`)

---

## 📝 Лицензия

Licensed under the MIT License. See [LICENSE](./LICENSE) for details.

© 2025