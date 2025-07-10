# 🚀 flask-urp-solution 教务自动化平台

## 📘 项目简介

`flask-urp-solution` 是一个基于 Flask 开发的教务系统自动化工具，专为高校师生设计，提供成绩查询、绩点统计与课程评估等一站式便捷服务，提升教务操作效率与用户体验。

---

## 🎯 核心功能⭐

- 🔍 **成绩查询**：登录后自动抓取并展示所有课程成绩及详细信息  
- 🎓 **绩点统计**：计算学期平均绩点、学分加权绩点、学位绩点等  
- 🧠 **评教助手**：支持查询评教任务，并一键自动完成评教流程  
- 🔐 **权限控制**：通过白名单机制控制用户访问，未授权用户将被拒绝服务并记录访问信息  
- 💻 **响应式前端**：界面简洁美观，适配移动端设备，交互友好

---

## 🛠️ 技术栈

| 类型     | 技术/库              |
|----------|----------------------|
| 后端     | Python 3, Flask      |
| 前端     | Bootstrap, 原生 JavaScript |
| 数据处理 | Pandas               |
| 其他     | DdddOcr, requests, BeautifulSoup4, colorama |

---
提交步骤

0. git pull origin main --allow-unrelated-histories
1. git add .
2. git commit -m "提交信息"
3. git push origin main
---

## ⚡ 快速开始

1. 📥 克隆项目
   ```bash
   git clone https://github.com/DaBao-Lee/flask-urp-solution.git
   cd flask-urp-solution
   ```

2. 📦 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. ▶️ 运行项目
   ```bash
   python main.py
   ```
   默认运行于：`http://127.0.0.1:5000`

---

## 🧭 项目结构

```plaintext
flask-urp-solution/
├── main.py            # 主程序入口
├── online.py          # 核心业务逻辑
├── static/            # 静态文件（CSS/JS/图像）
├── templates/         # 页面模板
├── requirements.txt   # 依赖列表
└── README.md          # 项目说明文档
```

---

## 🔌 接口说明

| 接口路径           | 功能描述             |
|--------------------|----------------------|
| `/grades`          | 查询课程成绩         |
| `/credits`         | 获取绩点与加权统计   |
| `/evaluationInfo`  | 获取评教任务信息     |
| `/evaluation`      | 自动完成评教任务     |

---

## 🖼️ 页面截图

> 📌 部署成功后可粘贴系统截图展示界面

---

## 🧱 使用说明与注意事项

- 教务系统数据源涉及用户账号，请妥善保管  
- 若学校教务系统结构发生变化，请及时同步更新代码  
- 所有用户数据仅做本地处理，不上传远端  
- 未授权用户将被记录，并自动禁止访问服务

---

## 📜 License

本项目基于 **MIT License** 开源

---

## 💬 参与交流

欢迎在 [Issues](https://github.com/DaBao-Lee/flask-urp-solution/issues) 区提出问题或建议。  
项目持续维护中，欢迎 Star & Fork 🌟
