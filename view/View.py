import os

class View:
    @staticmethod
    def print_color(text, color="white"):
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "end": "\033[0m"
        }
        try:
            print(f"{colors.get(color, colors['white'])}{text}{colors['end']}")
        except:
            print(text)

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def print_header(title):
        View.clear_screen()
        View.print_color("=" * 60, "cyan")
        View.print_color(f"| {title:^56} |", "cyan")
        View.print_color("=" * 60, "cyan")

    @staticmethod
    def print_main_menu():
        View.print_header("学生信息管理系统")
        View.print_color("\n【 主菜单 】", "yellow")
        View.print_color("-" * 40, "yellow")
        menu_items = [
            ("1", "添加学生"),
            ("2", "查看学生列表"),
            ("3", "修改学生信息"),
            ("4", "删除学生"),
            ("5", "模糊搜索"),
            ("6", "按专业筛选"),
            ("7", "批量导出CSV"),
            ("8", "批量导入CSV"),
            ("0", "退出系统")
        ]
        for key, value in menu_items:
            View.print_color(f"  {key}. {value}", "white")
        View.print_color("-" * 40, "yellow")

    @staticmethod
    def get_input(prompt, required=True):
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            View.print_color("输入不能为空，请重新输入", "red")

    @staticmethod
    def get_int_input(prompt, min_val=None, max_val=None):
        while True:
            try:
                value = int(input(prompt).strip())
                if min_val is not None and value < min_val:
                    View.print_color(f"输入必须大于等于{min_val}", "red")
                    continue
                if max_val is not None and value > max_val:
                    View.print_color(f"输入必须小于等于{max_val}", "red")
                    continue
                return value
            except ValueError:
                View.print_color("请输入有效的数字", "red")

    @staticmethod
    def get_gender_input(prompt):
        while True:
            value = input(prompt).strip()
            if value in ['男', '女']:
                return value
            View.print_color("性别只能是'男'或'女'", "red")

    @staticmethod
    def print_student_list(students):
        if not students:
            View.print_color("【提示】暂无学生信息", "yellow")
            return
        
        View.print_color(f"\n【统计】共 {len(students)} 名学生", "blue")
        
        headers = ["序号", "学号", "姓名", "性别", "年龄", "专业", "班级", "电话", "邮箱"]
        col_widths = [6, 12, 10, 6, 6, 15, 12, 15, 20]
        
        View.print_color("-" * sum(col_widths) + "-" * (len(headers) - 1), "cyan")
        
        header_line = "|"
        for i, header in enumerate(headers):
            header_line += f" {header:{col_widths[i]}} |"
        View.print_color(header_line, "cyan")
        
        View.print_color("-" * sum(col_widths) + "-" * (len(headers) - 1), "cyan")
        
        for idx, s in enumerate(students, 1):
            row = f"| {idx:<{col_widths[0] - 1}} |"
            row += f" {s['student_id']:<{col_widths[1] - 1}} |"
            row += f" {s['name']:<{col_widths[2] - 1}} |"
            row += f" {s['gender']:<{col_widths[3] - 1}} |"
            row += f" {s['age']:<{col_widths[4] - 1}} |"
            row += f" {s['major']:<{col_widths[5] - 1}} |"
            row += f" {s['class_name']:<{col_widths[6] - 1}} |"
            row += f" {str(s.get('phone', '')):<{col_widths[7] - 1}} |"
            row += f" {str(s.get('email', '')):<{col_widths[8] - 1}} |"
            print(row)
        
        View.print_color("-" * sum(col_widths) + "-" * (len(headers) - 1), "cyan")

    @staticmethod
    def print_student_detail(student):
        if not student:
            View.print_color("【错误】未找到学生信息", "red")
            return
        
        View.print_header("学生详情")
        View.print_color("\n【基本信息】", "yellow")
        print(f"学号：{student['student_id']}")
        print(f"姓名：{student['name']}")
        print(f"性别：{student['gender']}")
        print(f"年龄：{student['age']}")
        print(f"专业：{student['major']}")
        print(f"班级：{student['class_name']}")
        print(f"联系电话：{student.get('phone', '未填写')}")
        print(f"邮箱：{student.get('email', '未填写')}")
        print(f"地址：{student.get('address', '未填写')}")
        print(f"创建时间：{student['created_at']}")

    @staticmethod
    def show_success(message):
        View.print_color(f"【成功】{message}", "green")

    @staticmethod
    def show_error(message):
        View.print_color(f"【错误】{message}", "red")

    @staticmethod
    def show_info(message):
        View.print_color(f"【提示】{message}", "yellow")

    @staticmethod
    def wait_for_enter():
        input("\n按回车键继续...")

    @staticmethod
    def confirm_action(message):
        while True:
            choice = input(f"{message} (y/N)：").strip().lower()
            if choice in ['y', 'n', '']:
                return choice == 'y'
            View.print_color("请输入'y'确认或'n'取消", "red")