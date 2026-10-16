FROM python:3.11-slim

# تنظیم کاربر
WORKDIR /app

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های requirements
COPY requirements.txt .

# نصب کتابخانه‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد اصلی
COPY main.py .

# ایجاد پورت
EXPOSE ${PORT:-8443}

# اجرا
CMD ["python", "main.py"]
