FROM node:14 AS frontend-build

# 设置工作目录
WORKDIR /app

# 复制前端项目文件
COPY package*.json ./
COPY babel.config.js ./
COPY .browserslistrc ./
COPY vue.config.js ./
COPY public ./public/
COPY src ./src/

# 安装依赖并构建前端
RUN npm install
RUN npm run build

# 后端Python镜像
FROM python:3.8.15-slim

# 设置工作目录
WORKDIR /app

# 复制Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制数据文件夹
COPY data /app/data/

# 创建output目录
RUN mkdir -p /app/output

# 从前端构建阶段复制dist文件夹
COPY --from=frontend-build /app/dist /app/dist

# 复制后端代码
COPY backend /app/backend/

# 设置环境变量
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 5000

# 设置工作目录
WORKDIR /app

# 运行应用
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "backend", "app:app"] 