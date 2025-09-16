import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import psycopg2
from config import AREA, AREA_FILE
from common_utils import merge_columns_hierarchical


def fetch_data_from_db():
    """从数据库获取数据（保持不变）"""
    db_config = {
        'host': 'localhost',
        'user': 'liuhaojun',
        'password': 'Stephencurry521',
        'database': 'postgres',
        'port': 5432,
    }
    
    table_name = f'{AREA}区域.import_list_zd'
    fields = ['standard_name','zd_duration','begin_time','end_time','measure_name','cd_code']
    order_by = ['standard_name','zd_duration','begin_time','end_time','measure_name']
    
    try:
        conn = psycopg2.connect(**db_config)
        # 修正2：用','.join()拼接排序列，生成正确的SQL语法
        sql = f"SELECT {', '.join(fields)} FROM {table_name} ORDER BY {', '.join(order_by)}"
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"数据库错误: {e}")
        return None


if __name__ == "__main__":
    data_df = fetch_data_from_db()
    
    # 按层级合并的列顺序（重要：顺序决定层级关系）
    columns_to_merge = [
        'standard_name',
        'zd_duration',
        'begin_time',
        'end_time',
        'measure_name'
    ]

    # 自定义表头名称：键是原列名，值是想要显示的表头名称SS
    custom_headers = {
        'standard_name': '标准化名称',
        'zd_duration': '中断时长(分钟)',
        'begin_time': '生效开始时间',
        'end_time': '生效结束时间',
        'measure_name': '描述',
        'cd_code': '组合31位码'  # 确保所有列都有对应的表头名称
    }
    
    if data_df is not None:
        merge_columns_hierarchical(
            df=data_df,
            output_file=f'/Users/liuhaojun/Documents/项目文档/中国华电项目(云南)/03 时序数据质量稽核规则/{AREA_FILE}/00 总体/{AREA}区域_时序稽核质量规则_中断.xlsx',
            columns_to_merge=columns_to_merge,
            custom_headers=custom_headers  # 传递自定义表头
        )
