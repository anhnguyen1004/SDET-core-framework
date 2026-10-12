# 1. Bắt đầu với một môi trường Python tinh gọn
FROM python:3.11-slim

# 2. Đặt thư mục làm việc mặc định trong container
WORKDIR /app

# 3. Copy file thư viện vào trước để tận dụng Docker Cache
COPY requirements.txt .

# 4. Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Cài đặt Playwright và các thư viện lõi của hệ điều hành
RUN playwright install --with-deps chromium

# 6. Copy toàn bộ code test của bạn vào container
COPY . .

# 7. Lệnh mặc định sẽ được gọi khi khởi động container này
CMD ["pytest", "tests/"]