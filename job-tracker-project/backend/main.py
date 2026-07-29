from fastapi import FastAPI,Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from typing import Optional

#数据库连接
engine = create_engine("sqlite:///jobs.db",echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#数据表模型
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="未投递")
    apply_date = Column(String(50), nullable=True)
    job_url = Column(String(255), nullable=True)
    note = Column(String(500), nullable=True)

Base.metadata.create_all(engine)

#请求数据模型
class JobCreate(BaseModel):
    company:str
    position:str
    status:str = "未投递"
    apply_date:Optional[str] = None
    job_url:Optional[str] = None
    note:Optional[str] = None

class JobUpdate(BaseModel):
    company:Optional[str] = None
    position:Optional[str] = None
    status:Optional[str] = None
    apply_date:Optional[str] = None
    job_url:Optional[str] = None
    note:Optional[str] = None


#创建 FstAPI应用
app = FastAPI(title="Job Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#获取数据库对话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#查看所有岗位
@app.get("/jobs")
def read_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

#新增岗位
@app.post("/jobs")
def create_jobs(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(
        company = job.company,
        position = job.position,
        status = job.status,
        apply_date = job.apply_date,
        job_url = job.job_url,
        note = job.note,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

#删除岗位
@app.delete("/jobs/{job_id}")
def delete_jobs(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="岗位不存在")

    db.delete(job)
    db.commit()

    return {"message": "删除成功", "id": job_id}

#修改岗位接口
@app.put("/jobs/{job_id}")
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="岗位不存在")

    updata_data = job_update.dict(exclude_unset=True)
#循环导入到job数据库里面
    for key, value in updata_data.items():
        setattr(job,key,value)

    db.commit()
    db.refresh(job)

    return job