import subprocess
import sys

def run_script(script_path):
    """执行单个Python脚本"""
    try:
        # 使用当前Python解释器执行脚本
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ 脚本 {script_path} 执行成功")
        print("输出结果：")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 脚本 {script_path} 执行失败，错误码：{e.returncode}")
        print("错误信息：")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ 未找到脚本文件：{script_path}")
        return False

if __name__ == "__main__":
    # 定义要顺序执行的6个脚本路径（按执行顺序排列）
    scripts = [
        "Z1_生成稽核规则.py",
        "Z2_稽核规则导出_死值.py" ,
        "Z3_稽核规则导出_跳变.py" ,
        "Z4_稽核规则导出_越限.py" ,
        "Z5_稽核规则导出_中断.py" 
    ]
    
    print(f"开始执行脚本序列，共 {len(scripts)} 个脚本...")
    all_success = True
    
    # 循环执行每个脚本，前一个成功才执行下一个
    for i, script in enumerate(scripts, 1):
        print(f"\n--- 执行第 {i} 个脚本：{script} ---")
        if not run_script(script):
            all_success = False
            print(f"第 {i} 个脚本执行失败，终止后续脚本执行")
            break  # 一旦有脚本失败，停止执行后续脚本
    
    if all_success:
        print("\n所有脚本均执行成功！")
    else:
        print("\n脚本序列执行中断，部分脚本未执行")
    