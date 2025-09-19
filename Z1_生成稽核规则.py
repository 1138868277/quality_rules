import psycopg2
from psycopg2 import OperationalError
from config import AREA
from config import AREA_FILE
import os 

def create_connection(schema_name):  # 新增参数：模式名
    """创建数据库连接并指定默认模式"""
    connection = None
    try:
        connection = psycopg2.connect(
            database='postgres',
            user='liuhaojun',
            password='Stephencurry521',
            host='localhost',
            port=5432,
            # 关键：设置默认模式（search_path）
            options=f"-c search_path={schema_name}"
        )
        print(f"数据库连接成功！默认模式：{schema_name}")
    except OperationalError as e:
        print(f"连接错误: {e}")
    return connection

def execute_sql_script(connection, script_path):
    """读取并执行SQL脚本文件"""
    cursor = connection.cursor()
    try:
        # 读取SQL文件内容
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 执行脚本（会自动使用连接时指定的模式）
        cursor.execute(sql_script)
        connection.commit()
        print(f"脚本 {script_path} 执行成功")
    except Exception as e:
        connection.rollback()  # 出错时回滚
        print(f"脚本 {script_path} 执行失败: {e}")
    finally:
        cursor.close()

# 示例：在指定模式下执行多个SQL脚本
if __name__ == "__main__":
    # 指定要使用的模式名（替换为你的实际模式名）
    target_schema = f'{AREA}区域'  # 例如："wind_power_diagnosis"
    
    # 建立带模式的连接
    db_connection = create_connection(target_schema)

    if db_connection:
        sql_folder = "sql_scripts"
        # 要执行的脚本列表
        sql_scripts = [
            os.path.join(sql_folder, "清空表数据.sql"),
            os.path.join(sql_folder, "分级诊断_风电_死值.sql"),
            os.path.join(sql_folder, "分级诊断_风电_跳变.sql"),
            os.path.join(sql_folder, "分级诊断_风电_越限.sql"),
            os.path.join(sql_folder, "分级诊断_风电_中断.sql"),
            os.path.join(sql_folder, "分级诊断_光伏_死值.sql"),
            os.path.join(sql_folder, "分级诊断_光伏_跳变.sql"),
            os.path.join(sql_folder, "分级诊断_光伏_越限.sql"),
            os.path.join(sql_folder, "分级诊断_光伏_中断.sql"),
            os.path.join(sql_folder, "功率预测_风电_死值.sql"),
            os.path.join(sql_folder, "功率预测_风电_跳变.sql"),
            os.path.join(sql_folder, "功率预测_风电_越限.sql"),
            os.path.join(sql_folder, "功率预测_风电_中断.sql"),
            os.path.join(sql_folder, "功率预测_光伏_死值.sql"),
            os.path.join(sql_folder, "功率预测_光伏_跳变.sql"),
            os.path.join(sql_folder, "功率预测_光伏_越限.sql"),
            os.path.join(sql_folder, "功率预测_光伏_中断.sql")
        ]
        
        # 依次执行所有脚本
        for script in sql_scripts:
            execute_sql_script(db_connection, script)
        
        # 关闭连接
        db_connection.close()
        print("数据库连接已关闭")
