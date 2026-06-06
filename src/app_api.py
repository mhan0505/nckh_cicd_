import os
import sys
import json
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

# Sửa lỗi mã hóa console trên Windows (cp1252 -> UTF-8)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        # Nếu chạy trong môi trường không hỗ trợ reconfigure
        pass
    os.environ["PYTHONIOENCODING"] = "utf-8"


app = FastAPI(
    title="CI/CD Survey Analysis Webhook API",
    description="API webhook để kích hoạt tải dữ liệu Google Sheets và chạy pipeline phân tích dữ liệu khảo sát",
    version="1.0.0"
)

# Cấu hình CORS để cho phép gọi từ các domain khác nếu cần
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent.resolve()
RAW_FILE_PATH = BASE_DIR / "raw" / "CI_CD Survey Output - Student.csv"
STATUS_FILE_PATH = BASE_DIR / "scratch" / "pipeline_status.json"

# URL mặc định của Google Sheet dạng CSV
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1P_hyU6PUNp7ePHZQKY_G0aMwJgPjmxLhmhawHWjb_dY/export?format=csv&gid=135898341"

# Token bảo mật để tránh bị spam trigger (đọc từ Environment Variable, mặc định là chuỗi bí mật nếu không cấu hình)
SECURITY_TOKEN = os.getenv("WEBHOOK_TOKEN", "cicd_survey_secret_token_2026")

def update_status(status: str, error_msg: str = "", start_time: str = None, elapsed: float = None):
    """Cập nhật trạng thái chạy pipeline vào file JSON."""
    try:
        data = {}
        if STATUS_FILE_PATH.exists():
            with open(STATUS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        data["status"] = status
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if error_msg:
            data["last_error"] = error_msg
        if start_time:
            data["last_run_start"] = start_time
        if elapsed is not None:
            data["last_run_elapsed_seconds"] = round(elapsed, 2)
            
        STATUS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(STATUS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi khi ghi file trạng thái: {e}")

def run_pipeline_task(sheet_url: str):
    """Hàm chạy ngầm tải dữ liệu và thực thi pipeline."""
    start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = datetime.now()
    
    update_status("running", start_time=start_time_str)
    
    try:
        # Bước 1: Tải Google Sheet CSV và ghi đè vào thư mục raw/
        print(f"Bắt đầu tải dữ liệu từ Google Sheets: {sheet_url}")
        RAW_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Thêm User-Agent để tránh bị Google chặn request
        req = urllib.request.Request(
            sheet_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            csv_data = response.read()
            
        with open(RAW_FILE_PATH, "wb") as f:
            f.write(csv_data)
            
        print("Tải dữ liệu thành công, lưu vào raw/CI_CD Survey Output - Student.csv")
        
        # Bước 2: Thực thi file run_pipeline.py bằng subprocess để cô lập tiến trình
        print("Bắt đầu thực thi master pipeline (run_pipeline.py)...")
        pipeline_script = BASE_DIR / "run_pipeline.py"
        
        # Cấu hình môi trường UTF-8 cho subprocess
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        result = subprocess.run(
            [sys.executable, str(pipeline_script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(BASE_DIR),
            env=env
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            print("Pipeline chạy thành công!")
            update_status("success", elapsed=elapsed)
        else:
            print(f"Pipeline thất bại với mã lỗi {result.returncode}!")
            # Trích xuất lỗi từ stderr hoặc stdout
            error_details = result.stderr if result.stderr else result.stdout
            if len(error_details) > 1000:
                error_details = error_details[-1000:]
            update_status("failed", error_msg=error_details, elapsed=elapsed)
            
    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"Lỗi hệ thống khi chạy pipeline: {e}")
        update_status("failed", error_msg=str(e), elapsed=elapsed)

@app.post("/sync", summary="Kích hoạt đồng bộ dữ liệu và chạy phân tích")
async def trigger_sync(
    background_tasks: BackgroundTasks,
    token: str = Query(None, description="Token bảo mật để xác thực webhook"),
    x_token: str = Header(None, alias="X-Webhook-Token", description="Token bảo mật truyền qua Header"),
    sheet_url: str = Query(None, description="Link Google Sheet CSV tùy chỉnh (nếu muốn thay đổi)")
):
    # Xác thực bảo mật bằng token truyền qua Query Parameter hoặc Header
    provided_token = token or x_token
    if provided_token != SECURITY_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Token bảo mật không đúng hoặc thiếu."
        )
    
    # Kiểm tra xem có đang chạy dở không
    current_status = "idle"
    if STATUS_FILE_PATH.exists():
        try:
            with open(STATUS_FILE_PATH, "r", encoding="utf-8") as f:
                current_status = json.load(f).get("status", "idle")
        except:
            pass
            
    if current_status == "running":
        return {
            "status": "ignored",
            "message": "Pipeline hiện tại đang chạy. Vui lòng thử lại sau khi hoàn thành."
        }

    url_to_download = sheet_url if sheet_url else DEFAULT_SHEET_URL
    
    # Đưa tác vụ chạy pipeline vào background để trả kết quả HTTP ngay lập tức (không timeout)
    background_tasks.add_task(run_pipeline_task, url_to_download)
    
    return {
        "status": "processing",
        "message": "Đã nhận tín hiệu! Quy trình tải dữ liệu và chạy pipeline bắt đầu chạy ngầm."
    }

@app.get("/status", summary="Kiểm tra trạng thái chạy gần nhất của pipeline")
async def get_pipeline_status():
    if not STATUS_FILE_PATH.exists():
        return {
            "status": "idle",
            "message": "Pipeline chưa từng được chạy qua API."
        }
    try:
        with open(STATUS_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể đọc file trạng thái: {str(e)}")

@app.get("/", summary="Endpoint kiểm tra sức khỏe của API")
async def root():
    return {
        "app": "CI/CD Survey Analysis Webhook API",
        "status": "healthy",
        "default_sheet_url_configured": DEFAULT_SHEET_URL is not None
    }
