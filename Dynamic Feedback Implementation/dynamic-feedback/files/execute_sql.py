import sqlite3
import threading
import os
import sqlglot
# import sqlglot
# from configs.config import dev_databases_path



def execute_sql_threaded(sql, db_name, result_container):
    db_path = f"C:\\Users\\vamsi\\Documents\\1MTSU\\SEM 2\\Research Methods in Computer Science\\Research Project\\codebase\\RSL-SQL\\dynamic-feedback-test\\files\\test_database\\{db_name}\\{db_name}.sqlite"
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(sql)
        results = cursor.fetchall()
        result_container['row_count'] = len(results)
        result_container['column_count'] = len(results[0]) if results else 0
        result_container['result_preview'] = str(results[:5])
        # print("BLOCKER BOSS")
    except Exception as e:
        result_container['error'] = str(e)

    finally:
        if conn:
            conn.close()


def execute_sql(sql, db_name, timeout=30):
    result_container = {}
    thread = threading.Thread(target=execute_sql_threaded, args=(sql, db_name, result_container))
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # 超时处理
        return 0, 0, "TimeoutError: The SQL query took too long to execute. Please optimize your SQL query."
    else:
        # 返回结果
        if 'error' in result_container:
            return 0, 0, result_container['error']
        return result_container.get('row_count', 0), result_container.get('column_count', 0), result_container.get(
            'result_preview', "")
        
        
def extract_tables_and_columns(sql_query):
    parsed_query = sqlglot.parse_one(sql_query, read="sqlite")
    table_names = parsed_query.find_all(sqlglot.exp.Table)
    column_names = parsed_query.find_all(sqlglot.exp.Column)
    return {
        'table': {_table.name for _table in table_names},
        'column': {_column.alias_or_name for _column in column_names}
    }


def get_all_schema():
    # 读取所有数据库
    db_base_path = f"C:\\Users\\vamsi\\Documents\\1MTSU\\SEM 2\\Research Methods in Computer Science\\Research Project\\codebase\\RSL-SQL\\dynamic-feedback-test\\files\\test_database\\"
    db_schema = {}
    for db_name in os.listdir(db_base_path):
        db_path = os.path.join(db_base_path, db_name, db_name + '.sqlite')
        if os.path.exists(db_path):
            db_schema[db_name] = get_tables_and_columns(db_path)
    return db_schema

def get_tables_and_columns(sqlite_db_path):
    with sqlite3.connect(sqlite_db_path) as conn:
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return [
            f"{_table[0]}.{_column[1]}"
            for _table in tables
            for _column in cursor.execute(f"PRAGMA table_info('{_table[0]}');").fetchall()
        ]
