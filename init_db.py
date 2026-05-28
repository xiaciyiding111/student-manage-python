import sqlite3
import os

DB_FILE = "student_db.sqlite"

def init_database():
    try:
        os.makedirs(os.path.dirname(DB_FILE) if os.path.dirname(DB_FILE) else '.', exist_ok=True)
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            gender TEXT NOT NULL CHECK(gender IN ('男', '女')),
            age INTEGER NOT NULL CHECK(age > 0),
            major TEXT NOT NULL,
            class_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON students(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_major ON students(major)")
        
        conn.commit()
        conn.close()
        
        print("数据库和表初始化成功！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")

if __name__ == "__main__":
    init_database()