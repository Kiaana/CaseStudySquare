# Computational Physics Case Square

[简体中文](README.md) | English

## Introduction

Case Square is an online platform for showcasing and running Jupyter Notebook files, designed specifically for educational and learning scenarios. This platform allows teachers and students to upload their Jupyter Notebook assignments, categorize them for easy browsing, and run them online.

## Features

- **Categorized Display**: Display Jupyter Notebook files categorized by assignments or projects.
- **Run Online**: Execute Jupyter Notebook files directly on the website without configuring the local environment.
- **Data Bundling**: Each Jupyter Notebook file can include the data it needs to process, facilitating easy upload and download.
- **Isolated Runtime**: Each Jupyter Notebook file runs in a relatively isolated location, ensuring data security and stable operation.

## User Guide

1. **Upload Assignments**: Teachers or students can upload their Jupyter Notebook files and related data through the website's upload feature.
2. **Browse Assignments**: Users can browse all uploaded assignments on the homepage and filter by category.
3. **Run Assignments**: Click on any assignment to enter the online runtime environment and execute the Jupyter Notebook directly.

## Technical Details

- **Frontend**: Built with HTML and Bootstrap to provide an intuitive user experience.
- **Backend**: Uses the Flask framework to handle user requests and manage data.
- **Database**: Uses SQLite to store metadata of the assignments.
- **Storage**: Assignment files are stored in the server's file system.
- **Runtime Environment**: Uses MyBinder to provide an online runtime environment for Jupyter Notebook.

## Deployment Guide

This project is deployed using Docker. Ensure that Docker and Docker Compose are installed on your server.

1. Clone the repository to your server.
2. Run `docker-compose up --build` in the root directory of the project.
3. Visit `http://your-server-ip:1753`.

## Contribution Guide

If you have any suggestions or would like to contribute code, please submit an Issue or Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
