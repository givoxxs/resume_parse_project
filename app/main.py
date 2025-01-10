from fastapi import FastAPI, File, Request, UploadFile
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .utils.logger import logger
import uuid
from pathlib import Path
import os
import pandas as pd # type: ignore
from .services.resume_parse import parse_resume
from .utils.save_csv import save_to_csv
from urllib.parse import unquote

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting up.")
    yield
    logger.info("Application is shutting down.")

app = FastAPI(title="Document Processing API", lifespan=lifespan)

# Cấu hình CORS cho phép tất cả các domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các domain
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các header
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/check")
def read_check():
    return {"status": "ok"}
    
@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    file_paths = []
    results = []

    for file in files:
        try:
            # Tạo đường dẫn lưu file tạm
            file_path = UPLOAD_DIR / f"{uuid.uuid4()}{Path(file.filename).suffix}"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            # Phân tích file
            result = parse_resume(file_path)
            result['file_name'] = file.filename
            results.append(result)
            file_paths.append(str(file_path))

        except Exception as e:
            # Ghi lỗi nếu có vấn đề
            results.append({"file_name": file.filename, "error": str(e)})

    # Tạo tên file output CSV dựa trên timestamp
    timestamp = uuid.uuid4().hex[:8]  # Bạn cũng có thể dùng datetime.now()
    output_csv = RESULTS_DIR / f"output_{timestamp}.csv"
    try:
        save_to_csv(results, output_path=output_csv)
    except Exception as e:
        return {
            "Message": "Failed to save results to CSV",
            "error": str(e),
            "results": results,
        }

    # Xóa các file tạm sau khi xử lý
    for file_path in file_paths:
        if Path(file_path).exists():
            os.remove(file_path)

    return {
        "Message": "Files uploaded successfully",
        "results": results,
        "output_csv": str(output_csv),
    }   

            
@app.get("/download/results/{file_name}")
async def download_file(file_name: str):
    
    logger.info(f"Download file: {file_name}")
    file_path = RESULTS_DIR / file_name
  
    if file_path.exists():
        return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
    else:
        return {"error": f"File not found: {file_path}"}
            