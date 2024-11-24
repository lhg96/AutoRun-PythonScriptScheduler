from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import uvicorn
import os
import logging
from datetime import datetime
import json

# 로깅 설정
logging.basicConfig(
    filename='scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

class JobCreate(BaseModel):
    job_id: str
    script_path: str
    interval_value: int
    interval_unit: str

class JobUpdate(BaseModel):
    script_path: str
    interval_value: int
    interval_unit: str

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    job = scheduler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    interval = job.trigger.interval
    interval_value = 0
    interval_unit = "seconds"
    
    # 간격 단위 변환
    if interval.total_seconds() >= 3600 and interval.total_seconds() % 3600 == 0:
        interval_value = int(interval.total_seconds() / 3600)
        interval_unit = "hours"
    elif interval.total_seconds() >= 60 and interval.total_seconds() % 60 == 0:
        interval_value = int(interval.total_seconds() / 60)
        interval_unit = "minutes"
    else:
        interval_value = int(interval.total_seconds())
        interval_unit = "seconds"
    
    return {
        "id": job.id,
        "script_path": job.args[0],
        "interval_value": interval_value,
        "interval_unit": interval_unit,
        "next_run_time": str(job.next_run_time)
    }
    
@app.put("/api/jobs/{job_id}")
async def update_job(job_id: str, job_update: JobUpdate):
    try:
        old_job = scheduler.get_job(job_id)
        if not old_job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # 기존 작업 제거
        scheduler.remove_job(job_id)
        
        # 새로운 설정으로 작업 추가
        kwargs = {job_update.interval_unit: job_update.interval_value}
        scheduler.add_job(
            'scripts.run_script:run_script',
            'interval',
            id=job_id,
            args=[job_update.script_path],
            start_date='2024-01-01',
            **kwargs
        )
        
        logger.info(f"Job {job_id} updated successfully")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating job {job_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/logs")
async def get_logs(lines: int = 100):
    try:
        logs = []
        with open('scheduler.log', 'r') as f:
            logs = f.readlines()[-lines:]
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return {"logs": []}    

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.get("/api/jobs")
async def get_jobs():
    jobs = []
    for job in scheduler.get_jobs():
        interval = job.trigger.interval
        # 간격을 가장 적절한 단위로 변환
        if interval.total_seconds() < 60:
            interval_str = f"{int(interval.total_seconds())}초"
        elif interval.total_seconds() < 3600:
            interval_str = f"{int(interval.total_seconds() / 60)}분"
        else:
            interval_str = f"{int(interval.total_seconds() / 3600)}시간"
            
        jobs.append({
            'id': job.id,
            'next_run_time': str(job.next_run_time),
            'interval': interval_str
        })
    return jobs

@app.post("/api/jobs")
async def create_job(job: JobCreate):
    try:
        kwargs = {job.interval_unit: job.interval_value}
        scheduler.add_job(
            'scripts.run_script:run_script',
            'interval',
            id=job.job_id,
            args=[job.script_path],
            start_date='2024-01-01',
            **kwargs
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    try:
        scheduler.remove_job(job_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
