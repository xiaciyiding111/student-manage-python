import sqlite3
import os

class DBUtil:
    DB_FILE = "student_db.sqlite"

    @staticmethod
    def execute_sql(sql, params=None, fetch_one=False, fetch_all=False):
        conn = None
        cursor = None
        try:
            os.makedirs(os.path.dirname(DBUtil.DB_FILE) if os.path.dirname(DBUtil.DB_FILE) else '.', exist_ok=True)
            conn = sqlite3.connect(DBUtil.DB_FILE)
            
            if params:
                cursor = conn.execute(sql, params)
            else:
                cursor = conn.execute(sql)
            
            conn.commit()
            
            if fetch_one:
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
            elif fetch_all:
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in results]
            else:
                return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()