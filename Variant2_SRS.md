# Software Requirements Specification (SRS)

## 1. 文档信息
- 项目名称: Variant 2 - Child Play Time Evaluation Program
- 文档版本: v1.0
- 日期: 2026-04-15
- 依据课件:
  - Practical_lesson3_development_v3.pptx
  - Practical_lesson4_rest.pptx

## 2. 项目背景与目标
本项目用于评估儿童在 PC 上的游戏时间，依据任务列表控制和网络流量信息进行规则判定。

课件中给出的 Variant 2 目标链路如下:
- Get task list
- Get game list
- Check game start time
- Calc game duration
- Apply rules

课件中给出的同页任务还包括:
- Calculate a workload
- Save task list to file

系统形态根据课件允许二选一:
- REST service
- Telegram bot

本 SRS 采用 REST service 作为本项目默认实现形态，以满足后续 REST 课件实践任务。

## 3. 范围定义
### 3.1 In Scope
- 任务列表读取、保存、查询、更新
- 游戏列表读取、保存、查询、更新
- 游戏进程监控与启动时间记录
- 游戏时长计算
- Workload 计算
- 规则应用与结果输出
- REST API 暴露上述能力
- API 文档可访问
- Docker 容器化运行

### 3.2 Out of Scope
- 家长端移动应用
- 多设备账号同步
- 云端数据存储
- 自动封禁游戏进程的强制终止机制

## 4. 角色与使用者
- 家长/监护人: 维护任务和规则、查看统计结果
- 被监控用户(儿童): 受规则约束的游戏使用者
- 系统管理员(可与家长同一人): 部署和运行服务

## 5. 功能需求
### FR-01 获取任务列表 (Get task list)
- 系统应提供获取任务列表能力。
- 任务应至少包含:
  - 任务标识 `task_id`
  - 任务名称 `name`
  - 完成状态 `status` (done/todo)
  - 估计工作量字段 `workload_estimation`

### FR-02 保存任务列表到文件 (Save task list to file)
- 系统应支持将任务列表持久化到文件。
- 文件写入失败时应返回错误信息。

### FR-03 获取游戏列表 (Get game list)
- 系统应提供获取受控游戏列表能力。
- 游戏列表项应至少包含:
  - 游戏标识 `game_id`
  - 游戏名称 `name`
  - 进程名 `process_name`

### FR-04 监控游戏启动时间 (Check game start time)
- 系统应能检测受控游戏是否启动。
- 检测到启动时应记录启动时间 `start_time`。

### FR-05 计算游戏持续时间 (Calc game duration)
- 系统应基于启动时间和当前时间计算单次游戏时长。
- 系统应累计统计当日总游戏时长。

### FR-06 计算工作量 (Calculate a workload)
- 系统应基于任务列表计算 workload。
- workload 至少支持:
  - 总估计工作量
  - 已完成工作量
  - 完成率

### FR-07 应用规则 (Apply rules)
- 系统应根据任务完成情况、workload、游戏时长及网络流量指标进行规则判定。
- 判定结果应至少包括:
  - `allowed` (是否允许继续游戏)
  - `reason` (判定原因)

### FR-08 提供 REST 服务 (REST service)
- 系统应提供 REST API 访问以上核心能力。
- API 至少包含 `GET/POST/PUT/PATCH/DELETE` 中项目需要的方法。

### FR-09 API 文档可访问
- 系统应提供可访问的接口文档页面。
- 文档访问地址遵循 FastAPI 默认 `/docs`。

### FR-10 容器化部署
- 系统应可通过 Docker 构建镜像并运行。

## 6. 数据需求
### 6.1 任务实体 Task
- `task_id`: string
- `name`: string
- `status`: enum(todo, done)
- `workload_estimation`: number

### 6.2 游戏实体 Game
- `game_id`: string
- `name`: string
- `process_name`: string

### 6.3 会话实体 GameSession
- `session_id`: string
- `game_id`: string
- `start_time`: datetime
- `end_time`: datetime|null
- `duration_seconds`: number

### 6.4 规则判定实体 RuleDecision
- `decision_time`: datetime
- `allowed`: boolean
- `reason`: string

## 7. 接口需求 (REST)
以下为满足课件任务的最小接口集合。

### 7.1 Task API
- `GET /tasks`: 获取任务列表
- `POST /tasks`: 新建任务
- `PATCH /tasks/{task_id}`: 更新任务状态或工作量
- `DELETE /tasks/{task_id}`: 删除任务

### 7.2 Game API
- `GET /games`: 获取游戏列表
- `POST /games`: 新增受控游戏
- `DELETE /games/{game_id}`: 删除受控游戏

### 7.3 Monitor & Metrics API
- `GET /monitor/status`: 当前监控状态与正在运行游戏
- `GET /metrics/playtime`: 时长统计
- `GET /metrics/workload`: workload 统计

### 7.4 Rule API
- `GET /rules/decision`: 获取当前规则判定结果

## 8. 非功能需求
### NFR-01 可用性
- 服务应能在本机稳定运行。
- 服务异常应返回可读错误信息。

### NFR-02 性能
- 常规查询接口响应时间目标: 小于 1 秒(本机环境)。

### NFR-03 可维护性
- 代码应按模块组织: task、game、monitor、rules、api。

### NFR-04 安全性
- Token、密钥等敏感信息不得提交到 Git。

### NFR-05 可部署性
- 提供 Dockerfile。
- 支持标准命令完成构建和启动。

## 9. 约束与依赖
- 编程语言: Python
- REST 框架: FastAPI
- 服务启动: uvicorn
- 进程监控: 可使用 `psutil`
- 数据存储: 文件存储
- 运行平台: Windows 开发环境优先

## 10. 验收标准
项目验收应满足以下条目:
- 能运行 REST hello 服务。
- 能使用 curl 对关键接口发起请求并得到正确响应。
- 浏览器可访问 `/docs`。
- 应用中已集成 Variant 2 业务接口。
- 能构建并运行 Docker 容器。
- 功能上可完成:
  - Get task list
  - Get game list
  - Check game start time
  - Calc game duration
  - Apply rules
  - Calculate a workload
  - Save task list to file

## 11. 交付物映射 (来自课件)
- SRS: 本文档
- Backlog with time estimations: 待编写
- UI prototype: 待编写
- UML class diagram: 待编写

## 12. 术语
- SRS: Software Requirements Specification
- Workload: 任务工作量
- Playtime: 游戏时长

