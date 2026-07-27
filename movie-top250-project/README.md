# Movie Top 250 Project

一个 Python 爬虫 + FastAPI 小项目，用于抓取豆瓣 Top 250 电影数据并提供查询接口。

## 功能

- 爬取电影标题、评分和封面链接
- 保存到 SQLite 数据库
- 使用 io 获取电影海报的二进制数据，再传输到前端转化成图片展示
- 完善美化前端，添加筛选评分，添加电影海报封面、标题、评分，添加动画

## 技术栈

- Python
- requests
- BeautifulSoup
- SQLAlchemy
- FastAPI
- io
- uvicorn

