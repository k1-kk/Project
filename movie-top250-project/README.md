# 项目介绍

一个 Python 爬虫 + FastAPI 项目，用于抓取豆瓣 Top 250 电影数据并提供查询接口。

## 功能列表

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

## 项目结构

```txt
movie-top250-project/
├── backend/
│   ├── main.py              # FastAPI 后端接口
│   ├── spider_to_db.py      # 爬虫脚本，将电影数据写入 SQLite
│   └── requirements.txt     # 后端依赖
├── frontend/
│   ├── index.html           # 前端页面结构
│   ├── style.css            # 页面样式
│   └── app.js               # 调用接口并渲染电影卡片
├── README.md
├── .gitignore
└── movies.db                # 本地生成的数据库文件，不上传 GitHub
```

## 如何运行

- 1、进入项目目录
`cd movie-top250-project`
- 2、创建并激活虚拟环境
`python -m venv .venv`
- 3、安装依赖
`pip install -r backend/requirements.txt`
- 4、抓取电影数据
`python backend/spider_to_db.py`
- 5、启动后端服务
`uvicorn backend.main:app --reload`
- 6、打开前端页面
`frontend/index.html`

## API 接口示例

1、获取电影列表
```
GET /movies
```
- 支持参数
```
min_rating：最低评分，默认 0
max_rating：最高评分，默认 10
limit：返回数量，默认 10
```
- 示例
```
http://127.0.0.1:8000/movies?min_rating=9&max_rating=10&limit=20
```
2、图片代理接口
```
GET /proxy-image
```
- 示例
```
http://127.0.0.1:8000/proxy-image?url=图片地址
```

## 项目亮点

- 使用 Python 爬虫抓取真实网页数据
- 使用 SQLAlchemy 将数据保存到 SQLite
- 使用 FastAPI 提供后端查询接口
- 前端通过 fetch 调用接口并动态渲染页面
- 使用 /proxy-image 接口解决图片无法直接显示的问题
- 实现了前后端分离的基础项目结构

## 遇到的问题与解决方案
1. 图片无法显示</br>
豆瓣图片可能存在防盗链限制，前端直接使用 cover_url 时图片无法加载。</br>
解决方式：
后端新增 /proxy-image 接口，由 FastAPI 代理请求图片，再返回给前端显示。
2. 前端点击查询没有数据</br>
原因是 JavaScript 文件加载太早，页面按钮还没有渲染完成。</br>
解决方式：
把 <script src="./app.js"></script> 放到 body 底部，确保页面元素加载完成后再绑定点击事件。
3. 数据库路径读取错误</br>
后端移动到 backend/ 文件夹后，直接使用 sqlite:///movies.db 容易读错位置。</br>
解决方式：
使用 Path 生成稳定的数据库路径，让后端始终读取项目根目录下的 movies.db。
## 下一步计划
- 增加电影年份、导演、简介等字段
- 增加排序功能，例如按评分从高到低排序
- 增加加载中状态和错误提示样式
- 将前端页面进一步美化成完整电影数据看板
