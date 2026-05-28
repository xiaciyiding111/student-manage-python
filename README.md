# 学生信息管理系统

基于 Python + PyQt5 + SQLite 开发的学生信息管理系统，提供图形化界面和命令行两种操作方式。

## 功能特性

- ✅ **学生信息管理** - 添加、修改、删除学生信息
- ✅ **模糊搜索** - 支持按学号、姓名、专业、班级搜索
- ✅ **按专业筛选** - 快速筛选指定专业的学生
- ✅ **CSV导入导出** - 支持批量导入/导出学生数据，兼容Excel打开
- ✅ **数据持久化** - 使用SQLite数据库存储数据
- ✅ **图形界面** - 基于PyQt5的友好GUI界面
- ✅ **命令行界面** - 支持终端操作

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| PyQt5 | 5.15+ | 图形界面框架 |
| SQLite | 内置 | 数据库（无需额外安装） |
| PyInstaller | 6.0+ | 打包工具 |

## 项目结构

```
student-manage-python/
├── app.py                 # 图形界面主程序（PyQt5）
├── main.py                # 命令行版本主程序
├── init_db.py             # 数据库初始化脚本
├── config.py              # 配置文件
├── requirements.txt       # Python依赖列表
├── student_db.sqlite      # SQLite数据库文件（运行后自动创建）
├── dist/                  # 打包后的可执行文件目录
│   └── app.exe            # Windows可执行文件
├── exports/               # CSV导出目录
├── imports/               # CSV导入目录
├── utils/                 # 工具类
│   ├── DBUtil.py          # 数据库操作工具
│   └── FileUtil.py        # 文件操作工具（CSV导入导出）
├── dao/                   # 数据访问层
│   └── StudentDAO.py      # 学生数据访问对象
└── view/                  # 视图层
    └── View.py            # 命令行视图工具
```

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- Windows / macOS / Linux

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行方式

#### 方式1：图形界面（推荐）

```bash
python app.py
```

#### 方式2：命令行界面

```bash
python main.py
```

#### 方式3：可执行文件（Windows）

```bash
# 直接运行打包后的EXE文件
dist/app.exe
```

### 初始化数据库

首次运行前，建议先初始化数据库：

```bash
python init_db.py
```

## 使用说明

### 图形界面操作

1. **添加学生** - 点击工具栏「添加」按钮或菜单栏「编辑」→「添加学生」
2. **修改学生** - 选中表格中的学生，点击「修改」按钮或双击学生记录
3. **删除学生** - 选中学生后点击「删除」按钮，需要确认操作
4. **搜索功能** - 在搜索框输入关键词后按回车或点击搜索按钮
5. **专业筛选** - 从下拉框选择专业进行筛选
6. **CSV导出** - 菜单栏「文件」→「导出CSV」
7. **CSV导入** - 菜单栏「文件」→「导入CSV」

### CSV文件格式

导入的CSV文件需包含以下列（编码UTF-8）：

| 列名 | 必填 | 说明 |
|------|------|------|
| 学号 | 是 | 唯一标识，不能重复 |
| 姓名 | 是 | 学生姓名 |
| 性别 | 是 | 男/女 |
| 年龄 | 是 | 数字 |
| 专业 | 是 | 专业名称 |
| 班级 | 是 | 班级名称 |
| 联系电话 | 否 | 可选字段 |
| 邮箱 | 否 | 可选字段 |
| 地址 | 否 | 可选字段 |

## 打包成可执行文件

```bash
# 安装打包工具
pip install pyinstaller

# 打包成单文件
pyinstaller --onefile --windowed app.py

# 打包结果在 dist/ 目录下
```

## 配置说明

配置文件 `config.py`：

```python
CSV_CONFIG = {
    'export_path': './exports/',  # CSV导出路径
    'import_path': './imports/',  # CSV导入路径
    'encoding': 'utf-8-sig'       # 文件编码
}

TABLE_NAME = 'students'  # 数据库表名
```

## 项目架构

### 分层设计

```
┌─────────────────────────────────────────────────────────┐
│                    View Layer                           │
│  app.py (GUI)          main.py (CLI)                   │
├─────────────────────────────────────────────────────────┤
│                    Business Layer                       │
│  StudentDAO.py - 学生数据访问对象                        │
├─────────────────────────────────────────────────────────┤
│                    Data Layer                           │
│  DBUtil.py - 数据库操作工具                            │
│  FileUtil.py - 文件操作工具                            │
├─────────────────────────────────────────────────────────┤
│                    Database                             │
│  SQLite (student_db.sqlite)                            │
└─────────────────────────────────────────────────────────┘
```

### 主要类说明

| 类名 | 文件 | 说明 |
|------|------|------|
| StudentManagementApp | app.py | 图形界面主窗口 |
| StudentDialog | app.py | 添加/修改学生对话框 |
| StudentDAO | dao/StudentDAO.py | 学生数据访问对象 |
| DBUtil | utils/DBUtil.py | 数据库操作工具 |
| FileUtil | utils/FileUtil.py | CSV文件导入导出 |
| View | view/View.py | 命令行视图工具 |

## 数据库表结构

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL UNIQUE,  -- 学号
    name TEXT NOT NULL,               -- 姓名
    gender TEXT NOT NULL,             -- 性别
    age INTEGER NOT NULL,             -- 年龄
    major TEXT NOT NULL,              -- 专业
    class_name TEXT NOT NULL,         -- 班级
    phone TEXT,                       -- 联系电话
    email TEXT,                       -- 邮箱
    address TEXT,                     -- 地址
    created_at TIMESTAMP,             -- 创建时间
    updated_at TIMESTAMP              -- 更新时间
);
```

## 开发说明

### 添加新功能

1. 在 `StudentDAO.py` 中添加数据访问方法
2. 在 `app.py` 中添加界面组件和事件处理
3. 在 `main.py` 中添加命令行交互逻辑

### 代码规范

- 使用 PEP8 代码风格
- 类名使用 PascalCase
- 方法名和变量名使用 snake_case
- 添加必要的注释说明

## 许可证

MIT License

## 作者

Student Management System Development Team

---

**注意**：本项目为 Python 课程练习项目，用于学习和实践数据库操作、GUI开发和文件处理。