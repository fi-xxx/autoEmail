# Auto Email Scheduler

本项目可实现定时自动获取天气、每日一句，并通过邮件发送美观的 HTML 报告。

## 功能简介

- 每天定时（如 7:30）自动发送天气和温馨提醒邮件
- 天气信息来源于和风天气 API
- 支持幽默/温馨的女友视角提醒
- 邮件内容支持 HTML 美化
- 日志自动记录 API 调用、邮件发送等情况

## 快速部署

1. 克隆或上传本项目到服务器
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 配置 `config.py`（填写 API Key、邮箱等信息）
4. 启动定时任务：
   ```
   python scheduler/task_runner.py
   ```

## 目录结构

- `main.py`         主程序入口
- `scheduler/`      定时任务调度
- `utils/`          工具模块（天气、邮件、日志等）
- `logs/`           日志文件目录
- `config.py`       配置文件

## 说明

- 日志文件位于 `logs/auto_email.log`
- 如需自定义定时时间，请修改 `scheduler/task_runner.py`
- 支持 Windows/Linux 部署

---

嘿嘿~
