from view.View import View
from dao.StudentDAO import StudentDAO
from utils.FileUtil import FileUtil
from utils.DBUtil import DBUtil

class StudentManagementSystem:
    def __init__(self):
        self.view = View()

    def run(self):
        while True:
            self.view.print_main_menu()
            choice = input("请输入功能编号：").strip()
            
            try:
                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.view_students()
                elif choice == "3":
                    self.update_student()
                elif choice == "4":
                    self.delete_student()
                elif choice == "5":
                    self.search_students()
                elif choice == "6":
                    self.filter_by_major()
                elif choice == "7":
                    self.export_csv()
                elif choice == "8":
                    self.import_csv()
                elif choice == "0":
                    self.exit_system()
                    break
                else:
                    self.view.show_error("输入有误，请输入0-8之间的数字")
                    self.view.wait_for_enter()
            except Exception as e:
                self.view.show_error(f"操作失败: {e}")
                self.view.wait_for_enter()

    def add_student(self):
        self.view.print_header("添加学生")
        
        student = {
            'student_id': self.view.get_input("请输入学号："),
            'name': self.view.get_input("请输入姓名："),
            'gender': self.view.get_gender_input("请输入性别（男/女）："),
            'age': self.view.get_int_input("请输入年龄：", min_val=1, max_val=100),
            'major': self.view.get_input("请输入专业："),
            'class_name': self.view.get_input("请输入班级："),
            'phone': self.view.get_input("请输入联系电话（可选）：", required=False),
            'email': self.view.get_input("请输入邮箱（可选）：", required=False),
            'address': self.view.get_input("请输入地址（可选）：", required=False)
        }
        
        existing = StudentDAO.get_student_by_id(student['student_id'])
        if existing:
            self.view.show_error("该学号已存在")
            self.view.wait_for_enter()
            return
        
        StudentDAO.add_student(student)
        self.view.show_success("学生信息添加成功！")
        self.view.wait_for_enter()

    def view_students(self):
        self.view.print_header("学生列表")
        students = StudentDAO.get_all_students()
        self.view.print_student_list(students)
        self.view.wait_for_enter()

    def update_student(self):
        self.view.print_header("修改学生信息")
        
        student_id = self.view.get_input("请输入要修改的学生学号：")
        student = StudentDAO.get_student_by_id(student_id)
        
        if not student:
            self.view.show_error("未找到该学生")
            self.view.wait_for_enter()
            return
        
        self.view.print_student_detail(student)
        
        update_data = {}
        print("\n请输入要修改的信息（直接回车表示不修改）：")
        
        name = self.view.get_input(f"姓名（当前：{student['name']}）：", required=False)
        if name:
            update_data['name'] = name
        
        gender = self.view.get_input(f"性别（当前：{student['gender']}）：", required=False)
        if gender in ['男', '女']:
            update_data['gender'] = gender
        
        age_input = self.view.get_input(f"年龄（当前：{student['age']}）：", required=False)
        if age_input:
            try:
                age = int(age_input)
                if 1 <= age <= 100:
                    update_data['age'] = age
                else:
                    self.view.show_error("年龄必须在1-100之间")
            except ValueError:
                self.view.show_error("年龄必须是数字")
        
        major = self.view.get_input(f"专业（当前：{student['major']}）：", required=False)
        if major:
            update_data['major'] = major
        
        class_name = self.view.get_input(f"班级（当前：{student['class_name']}）：", required=False)
        if class_name:
            update_data['class_name'] = class_name
        
        phone = self.view.get_input(f"联系电话（当前：{student.get('phone', '')}）：", required=False)
        update_data['phone'] = phone if phone else None
        
        email = self.view.get_input(f"邮箱（当前：{student.get('email', '')}）：", required=False)
        update_data['email'] = email if email else None
        
        address = self.view.get_input(f"地址（当前：{student.get('address', '')}）：", required=False)
        update_data['address'] = address if address else None
        
        if update_data:
            StudentDAO.update_student(student_id, update_data)
            self.view.show_success("学生信息修改成功！")
        else:
            self.view.show_info("未修改任何信息")
        
        self.view.wait_for_enter()

    def delete_student(self):
        self.view.print_header("删除学生")
        
        student_id = self.view.get_input("请输入要删除的学生学号：")
        student = StudentDAO.get_student_by_id(student_id)
        
        if not student:
            self.view.show_error("未找到该学生")
            self.view.wait_for_enter()
            return
        
        self.view.print_student_detail(student)
        
        if self.view.confirm_action("确认删除该学生？"):
            StudentDAO.delete_student(student_id)
            self.view.show_success("学生信息删除成功！")
        else:
            self.view.show_info("取消删除")
        
        self.view.wait_for_enter()

    def search_students(self):
        self.view.print_header("模糊搜索")
        
        keyword = self.view.get_input("请输入搜索关键词（学号、姓名、专业或班级）：")
        students = StudentDAO.search_students(keyword)
        
        self.view.print_student_list(students)
        self.view.wait_for_enter()

    def filter_by_major(self):
        self.view.print_header("按专业筛选")
        
        majors = StudentDAO.get_all_majors()
        if not majors:
            self.view.show_info("暂无专业信息，请先添加学生")
            self.view.wait_for_enter()
            return
        
        self.view.print_color("\n【可用专业】", "yellow")
        for i, major in enumerate(majors, 1):
            print(f"  {i}. {major}")
        
        choice = self.view.get_int_input("\n请输入专业序号：", min_val=1, max_val=len(majors))
        selected_major = majors[choice - 1]
        
        students = StudentDAO.filter_by_major(selected_major)
        self.view.print_student_list(students)
        self.view.wait_for_enter()

    def export_csv(self):
        self.view.print_header("批量导出CSV")
        
        students = StudentDAO.get_all_students()
        if not students:
            self.view.show_info("暂无学生数据可导出")
            self.view.wait_for_enter()
            return
        
        filepath = FileUtil.export_to_csv(students)
        self.view.show_success(f"数据已成功导出到：{filepath}")
        self.view.show_info("导出的CSV文件可直接用Excel打开")
        self.view.wait_for_enter()

    def import_csv(self):
        self.view.print_header("批量导入CSV")
        
        filepath = self.view.get_input("请输入CSV文件路径：")
        
        try:
            students = FileUtil.import_from_csv(filepath)
        except Exception as e:
            self.view.show_error(str(e))
            self.view.wait_for_enter()
            return
        
        if not students:
            self.view.show_info("文件中没有有效的学生数据")
            self.view.wait_for_enter()
            return
        
        self.view.print_color(f"\n【待导入数据】共 {len(students)} 条记录", "yellow")
        self.view.print_student_list(students)
        
        if self.view.confirm_action("确认导入以上数据？"):
            success_count = 0
            fail_count = 0
            
            for student in students:
                try:
                    existing = StudentDAO.get_student_by_id(student['student_id'])
                    if existing:
                        fail_count += 1
                        continue
                    StudentDAO.add_student(student)
                    success_count += 1
                except Exception:
                    fail_count += 1
            
            self.view.show_success(f"导入完成！成功：{success_count}条，失败：{fail_count}条")
        else:
            self.view.show_info("取消导入")
        
        self.view.wait_for_enter()

    def exit_system(self):
        self.view.print_color("\n【再见】感谢使用学生信息管理系统！", "green")
        self.view.print_color("祝您生活愉快！", "green")

if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()
