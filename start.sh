#!/bin/bash

echo "=== KHỞI ĐỘNG HỆ THỐNG PHÂN TÍCH KHẢO SÁT CI/CD ==="

# 1. Khởi động FastAPI (Webhook Backend) trên port 8000
echo "--> Khởi động FastAPI Webhook..."
python -m uvicorn src.app_api:app --host 127.0.0.1 --port 8000 > /var/log/fastapi.log 2>&1 &
FASTAPI_PID=$!

# 2. Khởi động Streamlit (Interactive Dashboard) trên port 8501
echo "--> Khởi động Streamlit Dashboard..."
python -m streamlit run src/dashboard.py \
    --server.port 8501 \
    --server.address 127.0.0.1 \
    --browser.gatherUsageStats false \
    --server.headless true > /var/log/streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Đợi một vài giây để đảm bảo 2 ứng dụng đã khởi động
sleep 3

# Kiểm tra xem các tiến trình có chạy bình thường không
if ps -p $FASTAPI_PID > /dev/null; then
   echo "[OK] FastAPI đang chạy với PID $FASTAPI_PID"
else
   echo "[ERROR] FastAPI không khởi động thành công! Kiểm tra logs tại /var/log/fastapi.log"
   cat /var/log/fastapi.log
   exit 1
fi

if ps -p $STREAMLIT_PID > /dev/null; then
   echo "[OK] Streamlit đang chạy với PID $STREAMLIT_PID"
else
   echo "[ERROR] Streamlit không khởi động thành công! Kiểm tra logs tại /var/log/streamlit.log"
   cat /var/log/streamlit.log
   exit 1
fi

# 3. Khởi động Nginx (Reverse Proxy) ở chế độ Foreground (giữ container luôn sống)
echo "--> Khởi động Nginx Web Server..."
nginx -g "daemon off;"
