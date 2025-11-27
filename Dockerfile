# ใช้ Python base image
FROM python:3.11-slim

# ตั้ง working directory
WORKDIR /app

# ป้องกัน Python เขียน cache ไฟล์ .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดทั้งหมดเข้า container
COPY . .

# เปิด port 8000 (default ของ uvicorn)
EXPOSE 2000

# รัน FastAPI ด้วย Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2000"]
