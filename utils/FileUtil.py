import os
import csv
from datetime import datetime
from config import CSV_CONFIG

class FileUtil:
    @staticmethod
    def export_to_csv(students, filename=None):
        if not students:
            return None
        
        os.makedirs(CSV_CONFIG['export_path'], exist_ok=True)
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'students_{timestamp}.csv'
        
        filepath = os.path.join(CSV_CONFIG['export_path'], filename)
        
        headers = ['学号', '姓名', '性别', '年龄', '专业', '班级', '联系电话', '邮箱', '地址', '创建时间']
        
        try:
            with open(filepath, 'w', encoding=CSV_CONFIG['encoding'], newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for student in students:
                    row = [
                        student['student_id'],
                        student['name'],
                        student['gender'],
                        student['age'],
                        student['major'],
                        student['class_name'],
                        student.get('phone', ''),
                        student.get('email', ''),
                        student.get('address', ''),
                        student.get('created_at', '') if isinstance(student.get('created_at'), str) else (student['created_at'].strftime('%Y-%m-%d %H:%M:%S') if student['created_at'] else '')
                    ]
                    writer.writerow(row)
            
            return filepath
        except Exception as e:
            raise Exception(f"导出CSV失败: {e}")

    @staticmethod
    def import_from_csv(filepath):
        students = []
        
        if not os.path.exists(filepath):
            raise Exception("文件不存在")
        
        try:
            with open(filepath, 'r', encoding=CSV_CONFIG['encoding']) as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    student = {
                        'student_id': row.get('学号', '').strip(),
                        'name': row.get('姓名', '').strip(),
                        'gender': row.get('性别', '').strip(),
                        'age': int(row.get('年龄', 0)) if row.get('年龄', '').strip() else 0,
                        'major': row.get('专业', '').strip(),
                        'class_name': row.get('班级', '').strip(),
                        'phone': row.get('联系电话', '').strip() or None,
                        'email': row.get('邮箱', '').strip() or None,
                        'address': row.get('地址', '').strip() or None
                    }
                    
                    required_fields = ['student_id', 'name', 'gender', 'age', 'major', 'class_name']
                    if all(student.get(field) for field in required_fields if field != 'age') and student['age'] > 0:
                        students.append(student)
            
            return students
        except Exception as e:
            raise Exception(f"导入CSV失败: {e}")

    @staticmethod
    def list_export_files():
        files = []
        if os.path.exists(CSV_CONFIG['export_path']):
            for f in os.listdir(CSV_CONFIG['export_path']):
                if f.endswith('.csv'):
                    filepath = os.path.join(CSV_CONFIG['export_path'], f)
                    files.append({
                        'name': f,
                        'path': filepath,
                        'size': os.path.getsize(filepath),
                        'mtime': datetime.fromtimestamp(os.path.getmtime(filepath))
                    })
        return sorted(files, key=lambda x: x['mtime'], reverse=True)