# 【01】FastAPI 项目的渐进式构建思路

## 核心理念

本文的核心思路是**渐进式增强**——从一个极简的起点出发，逐步叠加必要的基础设施，最终形成一个可复用的项目模板。整个过程分为三个阶段：

### 🟢 起点：Hello World

- 仅包含 `main.py` 和一个测试文件
- 一个最简单的 FastAPI 路由，返回 "Hello World"
- 没有任何额外依赖，开箱即用

### 🟡 逐步增强

依次添加以下基础设施，每一步都独立且可控：

- **虚拟环境**：使用 Miniconda 隔离项目依赖，避免包冲突
- **代码规范（Linting）**：引入 `ruff` 或 `black` 等工具，统一代码风格
- **测试框架**：集成 `pytest`，编写并运行自动化测试
- **版本控制**：通过 Git 管理代码变更，配合 `.gitignore` 忽略虚拟环境等无关文件

### 终点：理想模板

最终达到一个"理想状态"——项目结构清晰、基础设施完备，可以作为任何新 FastAPI 项目的起点。在此基础上，你可以按需扩展：

- 无服务器架构（如 AWS Lambda）
- 数据科学项目
- REST API 开发
- 编程教育示例
- 作为新模板的起点

---

## 这种方式的优势

| 对比维度     | 传统"全功能模板"           | 渐进式最小项目             |
| ------------ | -------------------------- | -------------------------- |
| **透明度**   | 黑盒感强，不清楚各组件作用 | 每一步都亲手搭建，完全理解 |
| **可控性**   | 删除不需要的功能很麻烦     | 按需添加，没有冗余         |
| **学习成本** | 高，需要理解大量预置逻辑   | 低，从零开始逐步构建       |
| **灵活性**   | 受限于模板的设计决策       | 自由定制，适合各种场景     |

**核心理念**：与其找一个功能繁多却难以定制的模板，不如从一个极简的起点出发，亲手搭建出最贴合自身需求的项目结构。**少即是多**——每一行代码、每一个依赖，你都能清楚说出它存在的理由。

---

## 第一阶段：Hello World 起步

FastAPI 中最基本的 Hello World 项目由主文件（`main.py`）和测试文件（`test_hello_world.py`）组成：

```plaintext
hello_world
├── main.py
└── test_hello_world.py
```

### main.py

```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def say_hello() -> dict[str, str]:
    return {'message': 'Hello World'}
```

**注意**：代码中使用了 `dict[str, str]` 这种泛型语法，需要 **Python 3.9+** 版本支持。如果你使用的是 Python 3.8 及以下版本，需要改为 `from typing import Dict` 并使用 `Dict[str, str]`。

### 为什么 FastAPI 需要搭配 Uvicorn？

FastAPI 是一个基于 ASGI（异步服务器网关接口）的框架，它本身不是一个 Web 服务器，而是一个 Web 应用框架。要运行 FastAPI 应用，必须借助 ASGI 服务器，如 **Uvicorn** 或 **Hypercorn**。

Uvicorn 是一个高性能的 ASGI 服务器，基于 `uvloop` 和 `httptools` 构建，非常适合运行异步 Python 应用。

### 运行应用

由于没有特定的 Python 或 FastAPI 命令来运行应用程序，必须使用 ASGI Web 服务器。在虚拟环境中安装 FastAPI 和 Uvicorn：

```bash
(.venv) $ pip install fastapi "uvicorn[standard]"
```

然后运行 Uvicorn：

```bash
(.venv) $ uvicorn main:app --reload
```

**提示**：`--reload` 参数会在代码发生变化时自动重启服务器，仅建议在开发环境中使用，生产环境请勿开启。

运行后你将看到类似以下输出：

![image](https://boluo66.top/uploads/note-1790086055654-6d629fac-c311-4e13-a44f-36d02328e841.png)

### 验证接口

打开浏览器访问 `http://127.0.0.1:8000`，或使用命令行工具验证。

**使用 HTTPie**（需先安装：`pip install httpie`）：

![image](https://boluo66.top/uploads/note-1790086087866-6c7ea017-a3fc-4c92-80d4-c949222c29c6.png)

**使用 curl**（系统自带，无需安装）：

![image](https://boluo66.top/uploads/note-1790086117136-7f5eb825-0cef-4f73-845b-5d5109de6b69.png)

---

## 第二阶段：编写测试

### test_hello_world.py

```python

from fastapi.testclient import TestClient

from main import app 

# 创建测试客户端实例
client = TestClient(app)

# 编写标准的 pytest 测试函数（必须以 test_ 开头）
def test_read_main():
    response = client.get("/")
    # 4. 使用 assert 断言状态码和返回的 JSON 数据
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

**修正说明**：在新版 httpx 中，直接使用 `TestClient(app)` 会触发 `DeprecationWarning`。推荐使用 `ASGITransport` 显式指定传输层，这样可以消除警告并提高代码的可维护性。

### 安装测试依赖

```bash
(.venv) $ pip install pytest httpx==0.27.2
```

**修正说明**：原内容中 `pip install httpx=0.27.2` 使用了单等号 `=`，这是语法错误。pip 指定版本号应使用双等号 `==` 进行版本锁定。

### 运行测试

```bash
(.venv) $ pytest
```

预期输出：

![image](https://boluo66.top/uploads/note-1790086251333-31abd325-b505-4989-985f-39ee456078ea.png)

这两个文件对于一个说明性的例子来说已经足够了，但它们并不能构成一个可以在生产环境中使用的项目。我们将在接下来的部分中，基于软件工程最佳实践来改进该项目。

---

## 第三阶段：使用 Miniconda 管理虚拟环境

### 为什么需要虚拟环境？

在 Python 开发中，不同项目可能依赖不同版本的同一个库。如果所有项目都共用全局的 Python 环境，很容易产生包版本冲突。虚拟环境可以为每个项目创建独立的 Python 环境，确保依赖隔离。

### 为什么选择 Miniconda？

- **轻量级**：相比完整的 Anaconda，Miniconda 只包含 conda 包管理器和 Python，体积更小
- **跨平台**：支持 Windows、macOS 和 Linux
- **强大的依赖解析**：conda 的依赖解析器比 pip 更智能，能更好地处理复杂依赖关系
- **非 Python 包支持**：除了 Python 包，conda 还能管理 C 库、系统工具等非 Python 依赖

### 创建项目专属环境

1. **安装 Miniconda**：从 Miniconda 官网 下载并安装适合你操作系统的版本
2. **创建虚拟环境**：

```bash
# 创建一个名为 hello_fastapi 的环境，指定 Python 版本为 3.10
conda create -n hello_fastapi python=3.10 -y
```

3. **激活环境**：

```bash
# Windows
conda activate hello_fastapi
```

激活后，命令行提示符前会出现环境名称：

![image](https://boluo66.top/uploads/note-1790086479083-2cc21ec7-def6-4df9-a34f-85e16877e0c6.png)

4. **安装项目依赖**：

```bash
(hello_fastapi) $ pip install fastapi "uvicorn[standard]" pytest httpx==0.27.2
```

5. **导出环境配置**（方便团队协作或部署）：

```bash
# 导出为 environment.yml，Conda 环境管理的标准化配置文件。它的核心逻辑是将“当前计算机上所有的软件包、版本号及安装渠道”打包成一个可读的 YAML 文件
conda env export > environment.yml

# 团队成员使用，Conda 会读取该文件，在本地自动创建一个与开发者 A 完全一致（包括 Python 版本、所有依赖包及其精确版本号）的隔离环境。
conda env create -f environment.yml
```

6. **退出环境**：

```bash
conda deactivate
```

### 项目结构（含 Conda 配置）

```plaintext
hello_world
├── environment.yml        # Conda 环境配置文件
├── main.py                # FastAPI 主程序
└── test_hello_world.py    # 测试文件
```

### environment.yml 示例

![image](https://boluo66.top/uploads/note-1790263460931-c30200ea-53d7-4404-b5ab-0fac417515e0.png)

---

## 第四阶段：代码规范与 Linting

### 引入 Ruff

Ruff 是一个用 Rust 编写的超快速 Python linter 和代码格式化工具，可以替代 Flake8、Black、isort 等多个工具。

1. **安装 Ruff**：

```bash
(hello_fastapi) $ pip install ruff
```

2. **创建配置文件ruff.toml**：

![image](https://boluo66.top/uploads/note-1790263667570-9a1eff49-2b34-49eb-86f5-692601bb185c.png)


3. **运行检查**：

```bash
# 检查代码问题
(hello_fastapi) $ ruff check .

# 自动修复可修复的问题
(hello_fastapi) $ ruff check . --fix

# 格式化代码
(hello_fastapi) $ ruff format .
```

---

## 第五阶段：版本控制

### 在GitHub上创建仓库 Hello_FastAPI

![image](https://boluo66.top/uploads/note-1790265992043-58638e7c-bafa-42e8-b44f-afc3230e3442.png)

### 查询并配置用户名和邮箱

```bash
(hello_fastapi) $ git config --list
(hello_fastapi) $ git config user.name "你的用户名"
(hello_fastapi) $ git config user.email "你的邮箱"
```
![image](https://boluo66.top/uploads/note-1790266478325-1b9e07cd-5052-4cad-b102-093aabeb1cd1.png)
### 创建 .gitignore 文件

创建 `.gitignore` 文件，忽略不需要纳入版本控制的文件：

```gitignore
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
.venv/
venv/
ENV/
env/

# Conda
.envs/
*.conda_env

# IDE
.idea/
.vscode/
*.swp
*.swo

# 测试
.pytest_cache/
.coverage
htmlcov/

# 操作系统
.DS_Store
Thumbs.db

# 日志
*.log
```

### 提交到 Hello_FastAPI 仓库
生成 SSH 密钥（如果没有的话）,（一直按回车即可，最后会显示密钥路径）：
```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```

将路径的文件内公钥内容添加到 GitHub，复制输出的内容，到 GitHub → Settings → SSH and GPG keys → New SSH key 中粘贴添加：

修改仓库地址为 SSH 格式：
```bash
git remote set-url origin git@github.com:chatmole314/Hello_FastAPI.git
```
再试推送：
```bash
git push -u origin main
```
![image](https://boluo66.top/uploads/note-1790267894355-3c5a4649-2add-4294-b882-d3d679b307fa.png)

---


## 最终项目结构

经过以上所有步骤，最终的项目结构如下：

```plaintext
hello_world/
├── .gitignore               # Git 忽略规则
├── environment.yml          # Conda 环境配置
├── main.py                  # FastAPI 主程序
├── ruff.toml                # Ruff 代码规范配置
└── test_hello_world.py      # 测试文件
```

---

## 结语

通过这种渐进式的方式，你不仅得到了一个功能完备的项目模板，更重要的是理解了每一层基础设施的作用和必要性。这种"亲手搭建"的过程，远比直接克隆一个现成模板更有价值——因为每一行配置、每一个依赖，你都清楚它存在的理由。

**少即是多，理解胜过复制。**