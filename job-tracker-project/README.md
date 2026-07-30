# 求职管理系统

一个用于记录和管理求职进度的全栈练习项目。  
项目使用 FastAPI 提供后端接口，SQLite 保存岗位数据，前端使用 HTML、CSS 和 JavaScript 实现岗位的新增、查看、编辑、删除和状态筛选。

## 功能

- 添加岗位记录
- 查看岗位列表
- 编辑岗位信息
- 删除岗位记录
- 按投递状态筛选岗位
- 记录公司名称、岗位名称、投递状态、投递日期、岗位链接和备注

## 技术栈

### 后端

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

### 前端

- HTML
- CSS
- JavaScript
- Fetch API

## 项目结构

```txt
job-tracker-project/
├── backend/
│   ├── main.py              # FastAPI 后端接口
│   ├── requirement.txt      # 后端依赖
│   └── jobs.db              # 本地数据库文件
├── frontend/
│   ├── index.html           # 页面结构
│   ├── style.css            # 页面样式
│   └── app.js               # 前端交互逻辑
└── README.md
```

## 如何运行

1. 进入项目目录
```bash
cd job-tracker-project
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
```

3. 安装依赖
```bash
pip install -r backend/requirement.txt
```

4. 启动后端服务
```bash
uvicorn backend.main:app --reload
```
5. 打开前端页面
```bash
frontend/index.html
```

## API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/jobs` | 获取岗位列表 |
| POST | `/jobs` | 新增岗位 |
| PUT | `/jobs/{job_id}` | 修改岗位 |
| DELETE | `/jobs/{job_id}` | 删除岗位 |

## 数据字段

| 字段 | 说明 |
|---|---|
| `id` | 岗位记录 ID |
| `company` | 公司名称 |
| `position` | 岗位名称 |
| `status` | 投递状态 |
| `apply_date` | 投递日期 |
| `job_url` | 岗位链接 |
| `note` | 备注 |

## 投递状态

项目目前支持以下状态：
- 未投递
- 已投递
- 面试中
- 已拒绝
- 已offer
## 项目亮点

- 使用 FastAPI 实现完整 CRUD 接口
- 使用 SQLAlchemy 操作 SQLite 数据库
- 前端通过 Fetch API 调用后端接口
- 实现前后端分离的基础项目结构
- 支持岗位状态筛选，方便管理求职进度
- 表单同时支持新增和编辑两种模式

## 遇到的问题与解决方案

1. 路由参数错误导致 422

    在 `PUT /jobs/{job_id}` 中，路径参数需要传入数字 ID。
如果传入 `{id}` 这样的字符串，会出现 `422 Unprocessable Entity`。

    解决方式：

    在 Swagger 或前端请求中传入真实数字，例如：
    ```txt
    /jobs/1
    ```
2. 字段名写错导致 500

    新增岗位时，曾经把 `apply_date` 写成了 `apply_status`，导致数据库模型中找不到对应字段。

    解决方式：

    保持 Pydantic 模型和 SQLAlchemy 模型字段名称一致。
3. 前端编辑功能如何复用表单

    新增和编辑岗位都使用同一个表单。
点击“编辑”时，将当前岗位数据填回表单，并记录正在编辑的 `job_id`。
提交时根据是否存在 `editingJobId`，决定调用 `POST /jobs` 还是 `PUT /jobs/{job_id}`。

## 下一步计划

- 增加按公司名或岗位名搜索
- 增加岗位统计面板
- 增加状态颜色区分
- 增加数据导出功能
- 后续尝试使用 React 重构前端