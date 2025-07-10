# flask-urp-solution
 
## 项目简介

`flask-urp-solution` 是一个基于 Flask 的教务系统自动化工具，旨在为高校师生提供便捷的成绩查询、绩点统计与课程评估自动化服务。用户通过简单登录即可一站式完成教务相关操作，提升了教务管理效率和用户体验。

## 主要功能

- **成绩查询**：登录后可自动抓取并展示用户的所有课程成绩及详细信息。
- **绩点统计**：一键获取当前课程的绩点、学分绩点、加权学位绩点等信息。
- **评估信息展示与自动评教**：查询当前需要评教的课程与老师，支持一键自动完成所有评教任务。
- **权限管理**：通过白名单机制控制可用用户，未授权用户将被拒绝服务并记录登录信息。
- **前端美观交互**：采用响应式页面与简洁的界面，支持移动端访问，用户体验友好。

## 技术栈

- Python 3
- Flask
- 前端：Bootstrap + 原生 JS
- 数据处理：Pandas
- OCR 验证码识别：DdddOcr
- 依赖第三方库：requests, BeautifulSoup4, colorama

## 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/DaBao-Lee/flask-urp-solution.git
   cd flask-urp-solution
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行项目**
   ```bash
   python main.py
   ```
   默认服务运行在本地 `127.0.0.1:5000` 或指定主机端口。

4. **访问系统**
   打开浏览器输入 http://localhost:5000 登录系统。

## 目录结构

```
.
├── main.py                # Flask 主程序入口
├── online.py              # 业务逻辑与数据抓取
├── static/                # 前端静态文件（CSS/JS/图片）
├── templates/             # 页面模板（HTML）
├── requirements.txt       # Python 依赖
└── README.md
```

## 关键接口

- `/grades`         - 查询成绩（POST/GET）
- `/credits`        - 查询绩点信息
- `/evaluationInfo` - 获取评教信息
- `/evaluation`     - 自动评教

## 部分截图

（可根据实际部署后截图粘贴）

## 注意事项

- 本项目仅供学习交流，涉及教务系统账号信息请妥善保管。
- 对接的教务系统接口和页面结构如有变化，需同步调整代码。
- 所有用户信息仅做本地存储，未授权用户会被记录并拒绝访问。

## License

MIT License

---

如需二次开发或有任何疑问，欢迎在 ISSUES 区留言交流。
