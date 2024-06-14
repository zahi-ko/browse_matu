# browse_matu

[![GitHub Stars](https://img.shields.io/github/stars/zahi-ko/browse_matu?style=social)](https://github.com/zahi-ko/browse_matu)
[![GitHub Forks](https://img.shields.io/github/forks/zahi-ko/browse_matu?style=social)](https://github.com/zahi-ko/browse_matu/network/members)
[![GitHub License](https://img.shields.io/github/license/zahi-ko/browse_matu)](LICENSE)

`browse_matu`是一个Python脚本，用于自动化浏览和管理电子科技大学（UESTC）的MATU（Mathematics and Algorithm Training Utility）平台。

## 功能

- 自动登录MATU平台
- 收集作业列表、题目列表和已提交情况
- 下载代码文件并记录题目信息

## 安装

首先，确保您已经安装了Python和pip。然后，安装所需的依赖：

```bash
pip install requests beautifulsoup4
```

## 使用方法

1. 克隆仓库到本地机器
```bash
git clone https://github.com/zahi-ko/browse_matu.git
```
2. 进入项目目录
```bash
cd browse_matu
```
3. 根据你的matu账户信息，修改main函数中的用户名和密码
4. 运行脚本
```bash
python main.py
```

## 依赖

- requests：用于发送HTTP请求。
- beautifulsoup4：用于解析HTML文档。

## 贡献
如果您有任何建议或想要贡献代码，请提交Pull Request或创建Issue。