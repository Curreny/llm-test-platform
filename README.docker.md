# Docker 部署说明

本文档说明如何使用 Docker 部署大模型观测题库系统。

## 系统要求

- Docker 20.10.0 或更高版本
- Docker Compose 2.0.0 或更高版本
- 至少 2GB 可用内存
- 至少 5GB 可用存储空间

## 快速部署步骤

1. 克隆代码仓库:
   ```bash
   git clone https://github.com/your-username/llm-test-platform.git
   cd llm-test-platform
   ```

2. 使用 Docker Compose 构建和启动服务:
   ```bash
   docker-compose up -d
   ```

3. 访问应用:
   ```
   http://localhost:5000
   ```

## 自定义配置

### 修改端口

如果需要修改默认端口 (5000)，请编辑 `docker-compose.yml` 文件:

```yaml
ports:
  - "8080:5000"  # 将8080替换为您想要的端口
```

### 数据持久化

系统默认将以下目录挂载为卷，以保证数据持久化:

- `./data`: 保存题库 JSON 文件
- `./output`: 保存生成的输出文件

## 日志查看

查看应用日志:
```bash
docker-compose logs -f
```

## 停止和重启

停止服务:
```bash
docker-compose down
```

重启服务:
```bash
docker-compose restart
```

## 更新应用

如果有代码更新，请执行以下步骤:

1. 拉取最新代码:
   ```bash
   git pull
   ```

2. 重新构建并启动:
   ```bash
   docker-compose up -d --build
   ```

## 故障排除

### 容器无法启动

检查日志:
```bash
docker-compose logs
```

### 无法连接到应用

1. 确认容器正在运行:
   ```bash
   docker-compose ps
   ```

2. 检查网络配置:
   ```bash
   docker network ls
   ```

### 数据文件问题

确保 `data` 目录中包含所有必要的 JSON 文件:
- 100PoisonMpts_data.json
- CValues-Comparison_data.json
- instruction_attack_data.json
- SafetyBench_data.json
- typical_safety_data.json 