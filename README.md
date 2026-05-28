# 学生信息管理系统 · Python 课程练习

## 🎯 项目概述

基于 Python 开发的学生信息管理系统，提供图形界面和命令行两种操作方式。

## 🛠️ 技术栈

- **Python** - 主开发语言
- **SQLite** - 数据库管理
- **PyQt5** - 图形界面框架
- **文件处理** - CSV导入导出

## ✨ 核心功能

### 学生信息管理
- ✅ 添加学生信息
- ✅ 修改学生信息
- ✅ 删除学生信息
- ✅ 查看学生列表

### 搜索与筛选
- ✅ 模糊搜索（学号、姓名、专业、班级）
- ✅ 按专业筛选

### 数据导入导出
- ✅ 批量导出CSV文件（支持Excel打开）
- ✅ 批量导入CSV文件

### 系统特性
- ✅ 数据库连接管理（sqlite3）
- ✅ 输入数据校验与异常处理
- ✅ 模块化设计（DAO层与视图层分离）

## 🏗️ 项目结构

```
student-manage-python/
├── app.py                 # 图形界面主程序
├── main.py                # 命令行版本
├── init_db.py             # 数据库初始化
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── dao/
│   └── StudentDAO.py      # 数据访问层
├── utils/
│   ├── DBUtil.py          # 数据库操作工具
│   └── FileUtil.py        # CSV导入导出工具
└── view/
    └── View.py            # 命令行视图工具
```

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 运行图形界面
python app.py

# 或运行命令行版本
python main.py
```

## 📝 收获与体会

通过开发这个学生信息管理系统，我收获了以下经验：

1. **Python编程逻辑** - 熟练掌握了Python的基础语法和面向对象编程
2. **文件操作** - 学会了CSV文件的读写操作，支持Excel格式
3. **数据库交互** - 掌握了SQLite数据库的基本操作和连接管理
4. **代码调试** - 提升了调试技巧和问题解决能力
5. **系统设计** - 理解了模块化设计的重要性，实现了DAO层与视图层的分离

## 📄 许可证

MIT License
