# todo-api

基于 FastAPI 的待办清单 REST 接口，数据持久化到 JSON 文件。

## 功能

- 增删改查待办任务
- 标记完成 / 取消完成（PATCH）
- 文件损坏容错（自动回退空列表）
- 404 / 422 错误处理

## 技术栈

- Python 3.14
- FastAPI + pydantic（请求校验）
- uv（依赖管理）
- JSON 文件存储（无数据库）

## 快速开始

```bash
git clone https://github.com/HWWX5/todo-api.git
cd todo-api
uv sync
uvicorn main:app --reload
```

打开 http://127.0.0.1:8000/docs 查看交互式接口文档（FastAPI 自动生成）。

## 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 服务状态 |
| GET | `/todos` | 列出全部待办 |
| GET | `/todos/{id}` | 查询单条 |
| POST | `/todos` | 新增待办 |
| PATCH | `/todos/{id}` | 修改 task / done |
| DELETE | `/todos/{id}` | 删除待办 |

### 示例

**新增**

```bash
curl -X POST http://127.0.0.1:8000/todos \
     -H "Content-Type: application/json" \
     -d '{"task": "学 FastAPI"}'
```

响应：

```json
{"id": 1, "task": "学 FastAPI", "done": false}
```

**标记完成**

```bash
curl -X PATCH http://127.0.0.1:8000/todos/1 \
     -H "Content-Type: application/json" \
     -d '{"done": true}'
```

## 数据

存在 `todos.json`，结构：

```json
[
  {"id": 1, "task": "学 FastAPI", "done": true}
]
```

- `id` 自增，取当前最大值 + 1
- 文件不存在或损坏时自动返回空列表，不会崩溃
- PATCH 只改传入的字段，未传字段保持不变

## 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 404 | 待办不存在 |
| 422 | 请求参数错误（FastAPI 自动校验） |
