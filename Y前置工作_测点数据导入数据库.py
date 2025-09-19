import pandas as pd
import psycopg2
from psycopg2 import OperationalError, sql

def create_db_connection():
    """创建数据库连接"""
    try:
        connection = psycopg2.connect(
            database='postgres',
            user='liuhaojun',
            password='Stephencurry521',
            host='localhost',
            port=5432,
        )
        print("数据库连接成功")
        return connection
    except OperationalError as e:
        print(f"数据库连接失败: {e}")
        return None

def read_excel_data(excel_path):
    """读取Excel中的测点编码和测点描述列"""
    try:
        # 读取Excel文件，只选择需要的两列
        df = pd.read_excel(
            excel_path,
            usecols=["测点编码", "测点描述"],  # 只读取这两列
            dtype=str  # 避免数字型编码被自动转换
        )
        
        # 去除空行
        df = df.dropna(subset=["测点编码"]).reset_index(drop=True)
        print(f"成功读取Excel数据，共 {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return None

def import_to_database(connection, df, table_name, schema_name=None):
    """将数据导入数据库表"""
    if connection is None or df is None or df.empty:
        print("无法执行导入操作：连接未建立或无数据")
        return False

    try:
        cursor = connection.cursor()
        
        # 构建表名（支持指定模式）
        full_table_name = sql.Identifier(schema_name, table_name) if schema_name else sql.Identifier(table_name)
        
        # 清空表（可选：根据需求决定是否保留原有数据）
        # cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(full_table_name))
        
        # 准备插入语句
        insert_query = sql.SQL("""
            INSERT INTO {} (cd_name, cd_code)
            VALUES (%s, %s)
        """).format(full_table_name)
        
        # 批量插入数据
        data_to_insert = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data_to_insert)
        
        connection.commit()
        print(f"成功导入 {len(data_to_insert)} 条记录到表 {full_table_name}")
        return True
        
    except Exception as e:
        connection.rollback()
        print(f"导入失败: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    # 配置参数
    excel_file_path = "/Users/liuhaojun/Documents/项目文档/中国华电项目(云南)/03 时序数据质量稽核规则/08 黔源/05 黔源原始数据/黔源时序测点.xlsx"  # 替换为你的Excel文件路径
    target_table = "measure_data"                # 替换为数据库中的目标表名
    target_schema = "黔源区域"                       # 如需要指定模式，替换为模式名，否则为None
    
    # 执行流程
    db_conn = create_db_connection()
    if db_conn:
        excel_data = read_excel_data(excel_file_path)
        if excel_data is not None:
            import_to_database(db_conn, excel_data, target_table, target_schema)
        db_conn.close()
        print("数据库连接已关闭")
