<a name="readme-top"></a>

<div align="center">

<img height="120" src="./img/logo.webp">

<h1>Physics Computational Methods Case Study Square</h1>

**Physics Computational Methods Case Study Square** is an online platform designed for educational and learning scenarios, focusing on displaying and running Jupyter Notebook files.

[Simplified Chinese](README.md) | English

<!-- SHIELD GROUP -->

[![](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Kiaana/CaseStudySquare)
[![](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Kiaana/CaseStudySquare/actions)
[![](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Kiaana/CaseStudySquare/blob/main/LICENSE)
[![](https://img.shields.io/badge/contributors-1-orange.svg)](https://github.com/Kiaana/CaseStudySquare/graphs/contributors)
[![](https://img.shields.io/badge/issues-0-red.svg)](https://github.com/Kiaana/CaseStudySquare/issues)<br/>
[![](https://img.shields.io/badge/forks-0-lightgrey.svg)](https://github.com/Kiaana/CaseStudySquare/network/members)
[![](https://img.shields.io/badge/stars-2-yellow.svg)](https://github.com/Kiaana/CaseStudySquare/stargazers)

**Share Physics Computational Methods Case Study Square**

[![](https://img.shields.io/badge/share-WeChat-green.svg)](https://wechat.com)
[![](https://img.shields.io/badge/share-QQ-blue.svg)](https://qq.com)
[![](https://img.shields.io/badge/share-Weibo-red.svg)](https://weibo.com)

![](https://your-image-source.com/path/to/your/image.jpg)

</div>

<details>
<summary><kbd>Table of Contents</kbd></summary>

#### Table of Contents

- [👋🏻 Introduction](#-introduction)
- [✨ Features](#-features)
- [📘 User Guide](#-user-guide)
- [🛠 Technical Details](#-technical-details)
- [🚀 Deployment Guide](#-deployment-guide)
- [🤝 Contribution Guide](#-contribution-guide)
- [📄 License](#-license)

</details>

# Physics Computational Methods Case Study Square

Simplified Chinese | [English](README-en.md)

## Introduction

**Physics Computational Methods Case Study Square** is an online platform designed for educational and learning scenarios, focusing on displaying and running Jupyter Notebook files. We provide a convenient environment where teachers and students can upload their Jupyter Notebook assignments, categorize them, and make them easily accessible for others to browse and run.

## 💡 Features

- **Categorized Display**: We categorize Jupyter Notebook files by each assignment or project, making it easier to find and browse.
- **Run Online**: Users can run Jupyter Notebook files directly on our website without any configuration needed on their local environment.
- **Data Packaging**: Each Jupyter Notebook file can come with its required data for processing, making it convenient for uploading and downloading.
- **Isolated Running Environment**: We ensure that each Jupyter Notebook file runs in a relatively isolated location to ensure data security and stable operation.

## 📘 User Guide

1. **Upload Assignments**: Teachers or students can upload their Jupyter Notebook files and related data to the platform using our upload feature.
2. **Browse Assignments**: Users can browse all uploaded assignments on the homepage and can filter content they are interested in based on categories.
3. **Run Assignments**: Users can click on any assignment to enter the online running environment and directly run the Jupyter Notebook.

## 🛠 Technical Details

- **Frontend**: We have constructed an intuitive user interface using HTML and Bootstrap.
- **Backend**: We handle user requests and manage data using the Flask framework.
- **Database**: We use SQLite to store metadata of the assignments.
- **Storage**: Assignment files are stored in the file system of the server.
- **Running Environment**: We provide an online running environment for Jupyter Notebooks using MyBinder.

## 🚀 Deployment Guide

This project uses Docker for deployment. Please ensure that your server has Docker and Docker Compose installed.

1. Clone the repository to your server.
2. Run `docker-compose up --build` in the root directory of the project.
3. Visit `http://your-server-ip:1753`.

## 🤝 Contribution Guide

If you have any suggestions or would like to contribute code, please submit an Issue or Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
