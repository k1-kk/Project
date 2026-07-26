from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine,Column,Integer,String,Float
from sqlalchemy.orm import declarative_base,sessionmaker


# 定义数据库表结构（ORM模型）
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"        #数据库中的表名

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(100),nullable=False)
    rating = Column(Float,nullable=True)
    cover_url = Column(String(255),nullable=True)

# 创建数据库连接
engine = create_engine('sqlite:///movies.db',echo=False)     #echo=False表示不在控制台打印底层执行的SQL语句
#在数据库中创建这张表
Base.metadata.create_all(engine)

#创建会话工厂，和数据库交互
SessionLocal = sessionmaker(bind=engine)

# 爬取数据并存入数据库
def scrape_and_save_movies():
    session = SessionLocal()
    try:
        for start in range(0,250,25):
            url = f"https://movie.douban.com/top250?start={start}"
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                'Referer': "https://movie.douban.com/"
            }
            proxies = {'http':None,'https':None}

            response = requests.get(url,headers=headers,proxies=proxies,timeout=10)

        
            if response.status_code == 200:
                print(f"成功获取到网页第{start//25+1}页，开始解析内容")
            
                soup = BeautifulSoup(response.text,'html.parser')

                movie_items = soup.find_all("div",class_="item")

                for item in movie_items:
                    title = item.find("span",class_="title").text
                    rating_text = item.find("span",class_="rating_num").text
                    cover_url = item.find("img")["src"]

                    new_movie = Movie(
                        title = title,
                        rating = float(rating_text) if rating_text else 0.0,
                        cover_url = cover_url
                    )
                    session.add(new_movie)

            else:
                print(f"访问第{start//25+1}页出错，错误码为{response.status_code}")
            

            session.commit()
            print(f"所有电影保存完成")

    except Exception as e:
        session.rollback()
        print(f"抓取或入库失败：{e}")

    finally:
        session.close()

if __name__ == "__main__":
    scrape_and_save_movies()