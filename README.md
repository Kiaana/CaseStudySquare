# 物理计算方法案例广场

简体中文 | [English](README-en.md)

## 介绍

案例广场是一个用于展示和运行Jupyter Notebook文件的在线平台，专为教育和学习场景设计。本平台允许教师和学生上传他们的Jupyter Notebook作业，并将其分类整理，以便其他人浏览和运行。

## 特点

- **分类展示**：根据每次作业或项目来分类展示Jupyter Notebook文件。
- **在线运行**：直接在网站上运行Jupyter Notebook文件，无需在本地环境配置。
- **数据打包**：每个Jupyter Notebook文件可以附带其需要处理的数据，方便上传和下载。
- **独立运行环境**：每个Jupyter Notebook文件在一个相对独立的位置运行，确保数据安全和运行稳定。

## 使用指南

1. **上传作业**：教师或学生可以通过网站的上传功能，上传他们的Jupyter Notebook文件和相关数据。
2. **浏览作业**：用户可以在首页浏览所有已上传的作业，并根据分类来筛选。
3. **运行作业**：点击任一作业，即可进入在线运行环境，直接运行Jupyter Notebook。

## 技术细节

- **前端**：使用HTML和Bootstrap构建用户界面，提供直观的用户体验。
- **后端**：使用Flask框架处理用户请求和管理数据。
- **数据库**：使用SQLite存储作业的元数据。
- **存储**：作业文件存储在服务器的文件系统中。
- **运行环境**：使用MyBinder提供Jupyter Notebook的在线运行环境。

## 部署指南

本项目使用Docker进行部署，确保你的服务器已安装Docker和Docker Compose。

1. 克隆仓库到服务器。
2. 在项目根目录下运行`docker-compose up --build`。
3. 访问`http://your-server-ip:1753`。

## 贡献指南

如果你有任何建议或想要贡献代码，请提交Issue或Pull Request。

## 许可证

本项目采用[MIT许可证](LICENSE)。
