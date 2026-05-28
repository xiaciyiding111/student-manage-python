import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QComboBox, QSpinBox, QMessageBox, QFileDialog,
    QMenuBar, QMenu, QAction, QStatusBar, QGroupBox, QFormLayout,
    QDialog, QDialogButtonBox
)

from dao.StudentDAO import StudentDAO
from utils.FileUtil import FileUtil

class StudentManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_students()
    
    def init_ui(self):
        self.setWindowTitle("学生信息管理系统")
        self.setGeometry(100, 100, 1000, 600)
        
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_main_layout()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("欢迎使用学生信息管理系统")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = QMenu("文件(&F)", self)
        export_action = QAction("导出CSV", self)
        export_action.triggered.connect(self.export_csv)
        import_action = QAction("导入CSV", self)
        import_action.triggered.connect(self.import_csv)
        exit_action = QAction("退出(&Q)", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        edit_menu = QMenu("编辑(&E)", self)
        add_action = QAction("添加学生", self)
        add_action.triggered.connect(self.add_student_dialog)
        edit_action = QAction("修改学生", self)
        edit_action.triggered.connect(self.edit_student_dialog)
        delete_action = QAction("删除学生", self)
        delete_action.triggered.connect(self.delete_student)
        edit_menu.addAction(add_action)
        edit_menu.addAction(edit_action)
        edit_menu.addAction(delete_action)
        
        view_menu = QMenu("视图(&V)", self)
        refresh_action = QAction("刷新列表", self)
        refresh_action.triggered.connect(self.load_students)
        view_menu.addAction(refresh_action)
        
        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(view_menu)
    
    def create_tool_bar(self):
        toolbar = self.addToolBar("工具栏")
        toolbar.setMovable(False)
        
        add_btn = QPushButton("添加")
        add_btn.clicked.connect(self.add_student_dialog)
        toolbar.addWidget(add_btn)
        
        edit_btn = QPushButton("修改")
        edit_btn.clicked.connect(self.edit_student_dialog)
        toolbar.addWidget(edit_btn)
        
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_student)
        toolbar.addWidget(delete_btn)
        
        toolbar.addSeparator()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索学号、姓名、专业...")
        self.search_edit.returnPressed.connect(self.search_students)
        toolbar.addWidget(self.search_edit)
        
        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self.search_students)
        toolbar.addWidget(search_btn)
        
        self.major_combo = QComboBox()
        self.major_combo.addItem("全部专业")
        self.major_combo.currentTextChanged.connect(self.filter_by_major)
        toolbar.addWidget(self.major_combo)
    
    def create_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "学号", "姓名", "性别", "年龄", "专业", "班级", "电话", "邮箱", "地址"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_student_dialog)
        self.table.clicked.connect(self.show_student_detail)
        layout.addWidget(self.table)
        
        form_group = QGroupBox("学生详情")
        form_layout = QFormLayout(form_group)
        
        self.student_id_label = QLabel("-")
        self.name_label = QLabel("-")
        self.gender_label = QLabel("-")
        self.age_label = QLabel("-")
        self.major_label = QLabel("-")
        self.class_label = QLabel("-")
        self.phone_label = QLabel("-")
        self.email_label = QLabel("-")
        self.address_label = QLabel("-")
        
        form_layout.addRow("学号：", self.student_id_label)
        form_layout.addRow("姓名：", self.name_label)
        form_layout.addRow("性别：", self.gender_label)
        form_layout.addRow("年龄：", self.age_label)
        form_layout.addRow("专业：", self.major_label)
        form_layout.addRow("班级：", self.class_label)
        form_layout.addRow("电话：", self.phone_label)
        form_layout.addRow("邮箱：", self.email_label)
        form_layout.addRow("地址：", self.address_label)
        
        layout.addWidget(form_group)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)
    
    def load_students(self, students=None):
        if students is None:
            students = StudentDAO.get_all_students()
        
        self.table.setRowCount(0)
        
        for student in students:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(student['student_id']))
            self.table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.table.setItem(row, 2, QTableWidgetItem(student['gender']))
            self.table.setItem(row, 3, QTableWidgetItem(str(student['age'])))
            self.table.setItem(row, 4, QTableWidgetItem(student['major']))
            self.table.setItem(row, 5, QTableWidgetItem(student['class_name']))
            self.table.setItem(row, 6, QTableWidgetItem(student.get('phone', '')))
            self.table.setItem(row, 7, QTableWidgetItem(student.get('email', '')))
            self.table.setItem(row, 8, QTableWidgetItem(student.get('address', '')))
        
        self.table.resizeColumnsToContents()
        self.update_major_combo()
        self.status_bar.showMessage(f"共 {len(students)} 名学生")
    
    def update_major_combo(self):
        majors = StudentDAO.get_all_majors()
        current_text = self.major_combo.currentText()
        self.major_combo.blockSignals(True)
        self.major_combo.clear()
        self.major_combo.addItem("全部专业")
        self.major_combo.addItems(majors)
        self.major_combo.setCurrentText(current_text)
        self.major_combo.blockSignals(False)
    
    def search_students(self):
        keyword = self.search_edit.text().strip()
        if keyword:
            students = StudentDAO.search_students(keyword)
            self.load_students(students)
        else:
            self.load_students()
    
    def filter_by_major(self):
        major = self.major_combo.currentText()
        if major == "全部专业":
            self.load_students()
        else:
            students = StudentDAO.filter_by_major(major)
            self.load_students(students)
    
    def add_student_dialog(self):
        dialog = StudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            student = dialog.get_student_data()
            try:
                existing = StudentDAO.get_student_by_id(student['student_id'])
                if existing:
                    QMessageBox.warning(self, "警告", "该学号已存在！")
                    return
                
                StudentDAO.add_student(student)
                self.load_students()
                QMessageBox.information(self, "成功", "学生信息添加成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"添加失败：{str(e)}")
    
    def edit_student_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个学生！")
            return
        
        student_id = self.table.item(selected_row, 0).text()
        student = StudentDAO.get_student_by_id(student_id)
        
        if not student:
            QMessageBox.warning(self, "警告", "未找到学生信息！")
            return
        
        dialog = StudentDialog(self, student)
        if dialog.exec_() == QDialog.Accepted:
            update_data = dialog.get_update_data()
            try:
                StudentDAO.update_student(student_id, update_data)
                self.load_students()
                QMessageBox.information(self, "成功", "学生信息修改成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"修改失败：{str(e)}")
    
    def delete_student(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个学生！")
            return
        
        student_id = self.table.item(selected_row, 0).text()
        name = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除学生 {name}（学号：{student_id}）吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                StudentDAO.delete_student(student_id)
                self.load_students()
                QMessageBox.information(self, "成功", "学生信息删除成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败：{str(e)}")
    
    def export_csv(self):
        students = StudentDAO.get_all_students()
        if not students:
            QMessageBox.warning(self, "警告", "暂无学生数据可导出！")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "导出CSV文件", "", "CSV文件 (*.csv)"
        )
        
        if filepath:
            if not filepath.endswith('.csv'):
                filepath += '.csv'
            
            try:
                FileUtil.export_to_csv(students, os.path.basename(filepath))
                QMessageBox.information(self, "成功", f"数据已导出到：{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败：{str(e)}")
    
    def import_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "选择CSV文件", "", "CSV文件 (*.csv)"
        )
        
        if not filepath:
            return
        
        try:
            students = FileUtil.import_from_csv(filepath)
            if not students:
                QMessageBox.warning(self, "警告", "文件中没有有效的学生数据！")
                return
            
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
            
            self.load_students()
            QMessageBox.information(
                self, "导入完成", 
                f"导入完成！成功：{success_count}条，失败：{fail_count}条"
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入失败：{str(e)}")
    
    def show_student_detail(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.student_id_label.setText(self.table.item(selected_row, 0).text())
            self.name_label.setText(self.table.item(selected_row, 1).text())
            self.gender_label.setText(self.table.item(selected_row, 2).text())
            self.age_label.setText(self.table.item(selected_row, 3).text())
            self.major_label.setText(self.table.item(selected_row, 4).text())
            self.class_label.setText(self.table.item(selected_row, 5).text())
            self.phone_label.setText(self.table.item(selected_row, 6).text())
            self.email_label.setText(self.table.item(selected_row, 7).text())
            self.address_label.setText(self.table.item(selected_row, 8).text())
        else:
            self.student_id_label.setText("-")
            self.name_label.setText("-")
            self.gender_label.setText("-")
            self.age_label.setText("-")
            self.major_label.setText("-")
            self.class_label.setText("-")
            self.phone_label.setText("-")
            self.email_label.setText("-")
            self.address_label.setText("-")

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_dialog()
    
    def init_dialog(self):
        self.setWindowTitle("添加学生" if not self.student else "修改学生")
        self.setFixedSize(400, 400)
        
        self.student_id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 100)
        self.major_edit = QLineEdit()
        self.class_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.address_edit = QLineEdit()
        
        if self.student:
            self.student_id_edit.setText(self.student['student_id'])
            self.student_id_edit.setReadOnly(True)
            self.name_edit.setText(self.student['name'])
            self.gender_combo.setCurrentText(self.student['gender'])
            self.age_spin.setValue(self.student['age'])
            self.major_edit.setText(self.student['major'])
            self.class_edit.setText(self.student['class_name'])
            self.phone_edit.setText(self.student.get('phone', ''))
            self.email_edit.setText(self.student.get('email', ''))
            self.address_edit.setText(self.student.get('address', ''))
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("学号：", self.student_id_edit)
        form_layout.addRow("姓名：", self.name_edit)
        form_layout.addRow("性别：", self.gender_combo)
        form_layout.addRow("年龄：", self.age_spin)
        form_layout.addRow("专业：", self.major_edit)
        form_layout.addRow("班级：", self.class_edit)
        form_layout.addRow("电话：", self.phone_edit)
        form_layout.addRow("邮箱：", self.email_edit)
        form_layout.addRow("地址：", self.address_edit)
        
        layout.addLayout(form_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_student_data(self):
        return {
            'student_id': self.student_id_edit.text().strip(),
            'name': self.name_edit.text().strip(),
            'gender': self.gender_combo.currentText(),
            'age': self.age_spin.value(),
            'major': self.major_edit.text().strip(),
            'class_name': self.class_edit.text().strip(),
            'phone': self.phone_edit.text().strip() or None,
            'email': self.email_edit.text().strip() or None,
            'address': self.address_edit.text().strip() or None
        }
    
    def get_update_data(self):
        data = {}
        
        if self.name_edit.text().strip():
            data['name'] = self.name_edit.text().strip()
        data['gender'] = self.gender_combo.currentText()
        data['age'] = self.age_spin.value()
        
        if self.major_edit.text().strip():
            data['major'] = self.major_edit.text().strip()
        if self.class_edit.text().strip():
            data['class_name'] = self.class_edit.text().strip()
        
        phone = self.phone_edit.text().strip()
        data['phone'] = phone if phone else None
        
        email = self.email_edit.text().strip()
        data['email'] = email if email else None
        
        address = self.address_edit.text().strip()
        data['address'] = address if address else None
        
        return data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagementApp()
    window.show()
    sys.exit(app.exec_())