from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine,Column,Integer,Float,String
from sqlalchemy.orm import declarative_base,sessionmaker,Session
import uvicorn
from fastapi.responses import StreamingResponse
from pathlib import Path

import requests
import io

#创建基础样式base       orm
Base = declarative_base()

class Movie(Base):
    #表名
    __tablename__ = 'movies'
    #列名
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String(100),nullable=False)
    rating = Column(Float,nullable=True)
    cover_url = Column(String(255),nullable=True)
#引擎
DB_PATH = Path(__file__).resolve().parent.parent / "movies.db"
engine = create_engine(f"sqlite:///{DB_PATH}",echo=False)
#工厂
SessionLocal = sessionmaker(bind=engine)

#创建一个FastAPI实例
app = FastAPI(title="my movie API")

#配置 CORS，允许所有来源访问你的 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许所有域名访问，生产环境中应替换为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],        # 允许所有 HTTP 方法 (GET, POST 等)
    allow_headers=["*"],        # 允许所有请求头
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取图片
@app.get("/proxy-image")
def proxy_image(url: str):
    """
    接收前端传来的豆瓣图片 URL，由后端伪装成浏览器去请求，然后把图片数据返回给前端。
    """
    # 伪装请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://movie.douban.com/'
    }

    try:
        session = requests.Session()
        session.trust_env = False

        # 后端去请求真正的图片
        response = session.get(url,headers=headers,timeout=10)
        response.raise_for_status()

        return StreamingResponse(
            io.BytesIO(response.content),
            media_type=response.headers.get("Content-Type", "image/jpeg")
        )
        # 如果请求成功
        # if response.status_code == 200:
        #     # 将图片的二进制数据转换成流，并设置正确的 Content-Type 告诉浏览器这是一张图片
        #     return StreamingResponse(io.BytesIO(response.content), media_type=response.headers.get('Content-Type', 'image/jpeg'))
        # else:
        #     return {"error": "获取图片失败"}
    except Exception as e:
         return {"error": str(e)}


@app.get("/movies")
def read_movies(
    min_rating: float = 0.0, # 默认最低 0 分
    max_rating: float = 10,
    limit: int = 10,         # 默认最多返回 10 条
    db: Session = Depends(get_db)
):
    # 1. 构建查询，加入过滤条件：电影评分在 min_rating 和 max_rating 之间
    query = db.query(Movie).filter(
        Movie.rating >= min_rating,
        Movie.rating <= max_rating
    )
    
    # 2. 加入限制条件：只取前 limit 条
    movies = query.limit(limit).all()

    return movies

if __name__ == "__main__":
    uvicorn.run(app,host='127.0.0.1',port=8000)
