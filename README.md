# TiebaSignIn - 百度贴吧自动签到

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

一个使用 Python 编写的百度贴吧自动签到脚本，特别设计用于在 GitHub Actions 上运行。

## ✨ 功能特性

*   **自动登录**: 使用 `BDUSS` 和 `PTOKEN` Cookie 进行登录验证。
*   **获取关注列表**: 自动获取用户所有关注的贴吧列表（支持分页）。
*   **逐一签到**: 遍历关注的贴吧列表，并调用签到接口进行签到。
*   **结果反馈**: 记录每个贴吧的签到成功或失败状态。
*   **模拟行为**: 在每次签到请求之间加入随机延时，模拟人类操作。
*   **GitHub Actions 优化**: 设计为方便地通过 GitHub Actions 定时执行。

## 🔧 环境要求

*   Python 3.12
*   所需的 Python 库 (详见 `requirements.txt`):
    *   `requests`
    *   `beautifulsoup4`
    *   `lxml`

## 🚀 快速开始

### 1. 使用 GitHub Actions (推荐⭐)

1. **Fork** 此仓库到你自己的 GitHub 账户。

2. 在你的仓库页面，转到 Settings -> Secrets and variables -> Actions。

3. 点击 New repository secret。

4. 创建两个 Secrets：

   - BDUSS: 值为你获取到的 BDUSS。
   - PTOKEN: 值为你获取到的 PTOKEN。

5. 仓库中应包含一个 GitHub Actions workflow 文件 (例如 .github/workflows/tieba-signin.yml)。如果没有，可以创建如下：

   ```yaml
   # .github/workflows/tieba-signin.yml
   name: Tieba Sign In
   
   on:
     push:
       branches: [ master ]
     pull_request:
       branches: [ master ]
   
   jobs:
     build:
       runs-on: ubuntu-latest
       env:
         BDUSS: ${{ secrets.BDUSS }}
         PTOKEN: ${{ secrets.PTOKEN }}
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.12'
         
         - name: 安装依赖项
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
   
         - name: 运行 Python 脚本
           run: python run.py
   ```

6. GitHub Actions 将会根据 schedule 或手动触发 (workflow_dispatch) 自动运行签到脚本。你可以在仓库的 Actions 标签页查看运行日志。

### 2.本地运行

#### 2.1. 克隆仓库

```bash
git clone --depth=1 https://github.com/pochenyun/TiebaSignIn.git
cd TiebaSignIn
```

#### 2.2. 安装依赖

```
pip install -r requirements.txt
```

#### 2.3. 配置 Cookie

此脚本需要两个关键的 Cookie 值来进行身份验证：BDUSS 和 PTOKEN。

**⚠️ 重要提示:** 切勿将你的 BDUSS 和 PTOKEN 硬编码到代码中或直接提交到 Git 仓库！推荐使用环境变量或 GitHub Secrets。

**如何获取 BDUSS 和 PTOKEN:**

1. 在你的网页浏览器中登录百度贴吧 ([passport.baidu.com](https://passport.baidu.com/))。
2. 打开浏览器的开发者工具 (通常按 F12)。
3. 切换到 "Application" (Chrome/Edge) 或 "Storage" (Firefox) 标签页。
4. 找到任一接口，在右侧的 Cookie 列表中找到名为 BDUSS 的条目，复制它的值 (Value)。
5. 同样地，找到名为 PTOKEN 的条目，复制它的值。
6. **请妥善保管你的 BDUSS 和 PTOKEN，不要泄露给他人。**

#### 2.4. 配置运行环境

设置环境变量 BDUSS 和 PTOKEN：

- **Linux / macOS:**

  ```
  export BDUSS="你的BDUSS值"
  export PTOKEN="你的PTOKEN值"
  python run.py
  ```

- **Windows (Command Prompt):**

  ```
  set BDUSS="你的BDUSS值"
  set PTOKEN="你的PTOKEN值"
  python run.py
  ```

- **Windows (PowerShell):**

  ```
  $env:BDUSS="你的BDUSS值"
  $env:PTOKEN="你的PTOKEN值"
  python run.py
  ```

## 📝 日志

脚本运行时会将签到过程和结果输出到控制台（或 GitHub Actions 日志）。

## 📄 免责声明

- 本脚本仅供学习和技术交流使用。
- 用户需自行承担因使用此脚本可能带来的所有风险，包括但不限于账号被限制、API 更改导致脚本失效等。
- 请遵守百度贴吧的相关用户协议和规定。
- **强烈建议不要分享你的 BDUSS 和 PTOKEN 给任何人。**

