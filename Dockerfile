# Sử dụng image chính thức của Python
FROM python:3.9-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy các tệp requirements.txt vào container
COPY requirements.txt /app/

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào trong container
COPY . /app/

# Mở port 8000 mà ứng dụng sẽ chạy
EXPOSE 8000

# Lệnh chạy ứng dụng FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]