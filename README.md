
# 

  

## ساختار  پروژه


ساختار پروژه به شرح زیر است:

```

/

├── backend/ # کد بک‌اند FastAPI

│ ├── app/ # ماژول‌های برنامه

│ │ ├── __init__.py

│ │ ├── models.py # مدل‌های داده

│ │ ├── routes.py # مسیرهای API

│ │ └── database.py # اتصال به پایگاه داده

│ ├── Dockerfile # فایل داکر برای بک‌اند (خالی)

│ ├── main.py # نقطه ورود برنامه

│ └── requirements.txt # وابستگی‌های پایتون

└── docker-compose.yml # فایل داکر کامپوز (خالی)

```

  

  

  

## تکمیل فرآیند داکرایز کردن
  

### تکمیل Dockerfile برای بک‌اند (FastAPI)

  

فایل `backend/Dockerfile` را با محتوای زیر تکمیل کنید:
  

```dockerfile

# استفاده از تصویر پایه پایتون

FROM python:3.9-slim

  

# تنظیم دایرکتوری کاری

WORKDIR /app

  

# کپی فایل‌های وابستگی و نصب آن‌ها

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

  

# کپی کد برنامه

COPY . .

  

# تنظیم متغیرهای محیطی

ENV MONGODB_URL=mongodb://mongodb:27017/

ENV MONGODB_DB=taskdb

  

# اجرای برنامه

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

  

### تکمیل فایل docker-compose.yml

  

فایل `docker-compose.yml` در ریشه پروژه را با محتوای زیر تکمیل کنید:

  

```yaml

version: '3.8'

services:
  backend:
    build: ./backend
    container_name: fastapi_backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/
      - MONGODB_DB=taskdb
    depends_on:
      - mongodb
    networks:
      - app-network

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mongo-data:

```

  

### نکات تکمیلی برای تست و بررسی نصب داکرایز شده

  

1. برای ساخت و اجرای کانتینرها، دستور زیر را اجرا کنید:

```bash

docker-compose  up  --build

```

  

2. برای بررسی وضعیت کانتینرها:

```bash

docker-compose  ps

```

  

3. برای مشاهده لاگ‌ها:

```bash

docker-compose  logs  -f

```

  

4. برای توقف و حذف کانتینرها:

```bash

docker-compose  down

```

  

5. برای حفظ داده‌های MongoDB حتی پس از حذف کانتینرها، از volume استفاده شده است. برای حذف کامل داده‌ها:

```bash

docker-compose  down  -v

```

  

6. برای دسترسی به برنامه پس از راه‌اندازی:


- بک‌اند API: `http://localhost:8000`

- مستندات API: `http://localhost:8000/docs`

  

7. اطمینان حاصل کنید که پورت‌های، 8000 و 27017 روی سیستم شما در دسترس باشند و توسط سرویس دیگری استفاده نشوند.
