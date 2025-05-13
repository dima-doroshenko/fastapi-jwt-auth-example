## Установка

```bash
git clone https://github.com/dima-doroshenko/fastapi-jwt-auth-example
cd fastapi-jwt-auth-example
pip install -r requirements.txt
```

### .env

В файле .env должны быть ключи **`EMAIL_LOGIN`** и **`EMAIL_PASSWORD`**, в которых содержатся почта и пароль от аккаунта, который будет отправлять сообщения для верификации

### JWT

Сгенерируйте ключи для созданий JWT, поместите их по адресу **`certs\jwt-public.pem`** и **`certs\jwt-private.pem`**

### Тесты

Для проверки работы запустите тесты
```bash
pytest -v -s -c tests\pytest.ini
```

### Настройки

Файл настроек: **`src\config.py`**

## Запуск приложения

### Через `uvicorn`

```bash
uvicorn src.main:app --reload
```

### Через `Docker`


```bash
docker compose up --build
```
