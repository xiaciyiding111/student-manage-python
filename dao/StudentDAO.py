from utils.DBUtil import DBUtil
from config import TABLE_NAME

class StudentDAO:
    @staticmethod
    def add_student(student):
        sql = f"""
        INSERT INTO {TABLE_NAME} 
        (student_id, name, gender, age, major, class_name, phone, email, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            student['student_id'],
            student['name'],
            student['gender'],
            student['age'],
            student['major'],
            student['class_name'],
            student.get('phone'),
            student.get('email'),
            student.get('address')
        )
        return DBUtil.execute_sql(sql, params)

    @staticmethod
    def get_student_by_id(student_id):
        sql = f"SELECT * FROM {TABLE_NAME} WHERE student_id = ?"
        return DBUtil.execute_sql(sql, (student_id,), fetch_one=True)

    @staticmethod
    def get_all_students():
        sql = f"SELECT * FROM {TABLE_NAME} ORDER BY created_at DESC"
        return DBUtil.execute_sql(sql, fetch_all=True)

    @staticmethod
    def update_student(student_id, student_data):
        fields = []
        params = []
        
        if 'name' in student_data:
            fields.append('name = ?')
            params.append(student_data['name'])
        if 'gender' in student_data:
            fields.append('gender = ?')
            params.append(student_data['gender'])
        if 'age' in student_data:
            fields.append('age = ?')
            params.append(student_data['age'])
        if 'major' in student_data:
            fields.append('major = ?')
            params.append(student_data['major'])
        if 'class_name' in student_data:
            fields.append('class_name = ?')
            params.append(student_data['class_name'])
        if 'phone' in student_data:
            fields.append('phone = ?')
            params.append(student_data['phone'])
        if 'email' in student_data:
            fields.append('email = ?')
            params.append(student_data['email'])
        if 'address' in student_data:
            fields.append('address = ?')
            params.append(student_data['address'])
        
        if not fields:
            return 0
        
        params.append(student_id)
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(fields)} WHERE student_id = ?"
        return DBUtil.execute_sql(sql, params)

    @staticmethod
    def delete_student(student_id):
        sql = f"DELETE FROM {TABLE_NAME} WHERE student_id = ?"
        return DBUtil.execute_sql(sql, (student_id,))

    @staticmethod
    def search_students(keyword):
        sql = f"""
        SELECT * FROM {TABLE_NAME} 
        WHERE student_id LIKE ? OR name LIKE ? OR major LIKE ? OR class_name LIKE ?
        ORDER BY created_at DESC
        """
        pattern = f'%{keyword}%'
        params = (pattern, pattern, pattern, pattern)
        return DBUtil.execute_sql(sql, params, fetch_all=True)

    @staticmethod
    def filter_by_major(major):
        sql = f"SELECT * FROM {TABLE_NAME} WHERE major = ? ORDER BY created_at DESC"
        return DBUtil.execute_sql(sql, (major,), fetch_all=True)

    @staticmethod
    def get_all_majors():
        sql = f"SELECT DISTINCT major FROM {TABLE_NAME} ORDER BY major"
        result = DBUtil.execute_sql(sql, fetch_all=True)
        return [item['major'] for item in result]

    @staticmethod
    def count_students():
        sql = f"SELECT COUNT(*) as count FROM {TABLE_NAME}"
        result = DBUtil.execute_sql(sql, fetch_one=True)
        return result['count'] if result else 0