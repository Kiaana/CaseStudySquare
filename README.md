<a name="readme-top"></a>

<div align="center">

<img height="120" src="./logo.webp">

<h1>物理计算方法案例广场</h1>

**物理计算方法案例广场** 是一个为教育和学习场景设计的在线平台，专注于展示和运行 Jupyter Notebook 文件。

简体中文 | [English](README-en.md)

<!-- SHIELD GROUP -->

[![](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Kiaana/CaseStudySquare)
[![](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Kiaana/CaseStudySquare/actions)
[![](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Kiaana/CaseStudySquare/blob/main/LICENSE)
[![](https://img.shields.io/badge/contributors-1-orange.svg)](https://github.com/Kiaana/CaseStudySquare/graphs/contributors)
[![](https://img.shields.io/badge/issues-0-red.svg)](https://github.com/Kiaana/CaseStudySquare/issues)<br/>
[![](https://img.shields.io/badge/forks-0-lightgrey.svg)](https://github.com/Kiaana/CaseStudySquare/network/members)
[![](https://img.shields.io/badge/stars-2-yellow.svg)](https://github.com/Kiaana/CaseStudySquare/stargazers)

**分享物理计算方法案例广场**

[![](https://img.shields.io/badge/share-微信-green.svg)](https://wechat.com)
[![](https://img.shields.io/badge/share-QQ-blue.svg)](https://qq.com)
[![](https://img.shields.io/badge/share-微博-red.svg)](https://weibo.com)

![](https://your-image-source.com/path/to/your/image.jpg)

</div>

<details>
<summary><kbd>目录</kbd></summary>

#### 目录

- [👋🏻 介绍](#-介绍)
- [✨ 特点](#-特点)
- [📘 使用指南](#-使用指南)
- [🛠 技术细节](#-技术细节)
- [🚀 部署指南](#-部署指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)

</details>

# 物理计算方法案例广场

简体中文 | [English](README-en.md)

## 👋🏻 介绍

**物理计算方法案例广场** 是一个为教育和学习场景设计的在线平台，专注于展示和运行 Jupyter Notebook 文件。我们提供一个方便的环境，让教师和学生能够上传他们的 Jupyter Notebook 作业，并将其分类整理，以便其他人能够方便地浏览和运行。

## 💡 特点

- **分类展示**: 我们根据每次作业或项目来分类展示 Jupyter Notebook 文件，使其更易于查找和浏览。
- **在线运行**: 用户可以直接在我们的网站上运行 Jupyter Notebook 文件，无需在本地环境进行任何配置。
- **数据打包**: 每个 Jupyter Notebook 文件都可以附带其需要处理的数据，方便上传和下载。
- **独立运行环境**: 我们确保每个 Jupyter Notebook 文件在一个相对独立的位置运行，以确保数据安全和运行稳定。

## 📘 使用指南

1. **上传作业**: 教师或学生可以通过我们的上传功能，将他们的 Jupyter Notebook 文件和相关数据上传到平台。
2. **浏览作业**: 用户可以在首页浏览所有已上传的作业，并可以根据分类来筛选他们感兴趣的内容。
3. **运行作业**: 用户可以点击任一作业，进入在线运行环境，并直接运行 Jupyter Notebook。

## 🛠 技术细节

- **前端**: 我们使用 HTML、CSS、Javascript 和 Bootstrap 构建了一个直观的用户界面。
- **后端**: 我们使用 Flask 框架来处理用户请求并管理数据。
- **数据库**: 我们使用 SQLite 来存储作业的元数据。
- **存储**: 服务器自动将文件推送到GitHub或Gitee仓库进行存储。
- **运行环境**: 我们使用 MyBinder 提供 Jupyter Notebook 的在线运行环境。

## 🚀 部署指南

本项目使用 Docker 进行部署，请确保你的服务器已安装 Docker 和 Docker Compose。

1. 将仓库克隆到你的服务器。
2. 修改根目录下的`app.py`文件，将`GITHUB_TOKEN`和`GITEE_TOKEN`的值改为你的 GitHub 或 Gitee 仓库的 Token，并将`GITHUB_REPO`和`GITEE_REPO`的值改为你的 GitHub 或 Gitee 仓库的地址。
3. 设置`GITHUB_OR_GITEE`的值为`github`或`gitee`，以指定使用 GitHub 还是 Gitee 作为仓库。国内推荐使用 Gitee，传输比较稳定，避免服务器无法连接 GitHub。
4. 在项目根目录下运行 `docker-compose up --build`。
5. 访问 `http://your-server-ip:1753`。

## 🤝 贡献指南

如果你有任何建议或想要贡献代码，请提交 Issue 或 Pull Request。

## 📄 许可证

本项目采用 [MIT许可证](LICENSE)。
