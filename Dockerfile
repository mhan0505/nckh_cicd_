# Sử dụng Python 3.10 slim làm base image
FROM python:3.10-slim

# Ngăn Python viết các file pyc và giữ stdout/stderr không bị buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (Nginx, procps cho script start.sh, git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    procps \
    git \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt và cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy file cấu hình Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copy toàn bộ mã nguồn và thư mục dự án vào container
COPY src/ ./src/
COPY notebooks/ ./notebooks/
COPY raw/ ./raw/
COPY processed/ ./processed/
COPY interim/ ./interim/
COPY reports/ ./reports/
COPY docs/ ./docs/
COPY run_pipeline.py .
COPY start.sh .

# Tạo thư mục chứa các file tạm và cấu hình phân quyền
RUN mkdir -p scratch && chmod -R 777 scratch raw processed interim reports

# Cấp quyền thực thi cho file start.sh
RUN chmod +x start.sh

# Expose cổng 8080 (cổng Nginx công khai)
EXPOSE 8080

# Chạy file khởi động
CMD ["./start.sh"]
