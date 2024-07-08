import pandas as pd
import os


def clean_datetime(dt_string):
    try:
        return pd.to_datetime(dt_string).strftime('%Y-%m-%d %H:%M:%S')
    except:
        print(f"无法解析的日期时间: {dt_string}")
        return None


def process_csv(input_path, output_path):
    print(f"正在处理文件: {input_path}")

    if not os.path.exists(input_path):
        print(f"错误: 输入文件不存在 - {input_path}")
        return

    try:
        df = pd.read_csv(input_path)
        print(f"成功读取CSV文件，共 {len(df)} 行")

        if 'datetime' not in df.columns:
            print("错误: CSV文件中没有 'datetime' 列")
            return

        original_datetime = df['datetime'].copy()
        df['datetime'] = df['datetime'].apply(clean_datetime)

        # 检查处理前后的差异
        changes = (original_datetime != df['datetime']).sum()
        print(f"datetime 列中有 {changes} 个值被修改")

        # 检查是否有任何 None 值（无法解析的日期时间）
        null_count = df['datetime'].isnull().sum()
        if null_count > 0:
            print(f"警告: 有 {null_count} 个日期时间值无法解析")

        df.to_csv(output_path, index=False)
        print(f"处理后的文件已保存至: {output_path}")

    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")


if __name__ == "__main__":
    input_file = r"D:\Pycharm_pro\demo\pythonProject\pro_data\activity.csv"
    output_file = r"D:\Pycharm_pro\demo\pythonProject\pro_data\cleaned_activity.csv"
    process_csv(input_file, output_file)

    print("脚本执行完毕")