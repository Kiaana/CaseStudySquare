# 使用官方 Python 运行时作为父镜像
FROM python:3.12-slim

# 设置环境变量:
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
# - PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录 /app
WORKDIR /app

# 将当前目录内容复制到位于 /app 中的容器中
COPY . /app

# 安装任何需要的包
# RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
# 默认使用清华源
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 让端口 80 可供此容器外的环境使用
EXPOSE 80

# 定义环境变量
ENV NAME World

# 在容器启动时运行 app.py
CMD ["python", "app.py"]
