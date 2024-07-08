import pandas as pd
import uuid
from urllib.parse import urlparse
import os
from datetime import datetime

# 文件路径
http_path = 'D:/Pycharm_pro/demo/pythonProject/data/http.csv'
file_path = 'D:/Pycharm_pro/demo/pythonProject/data/file.csv'
email_path = 'D:/Pycharm_pro/demo/pythonProject/data/email.csv'
output_http_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/http_details.csv'
output_file_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/file_details.csv'
output_email_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/email_details.csv'


def process_http_details():
    http_df = pd.read_csv(http_path)
    http_df['http_id'] = [str(uuid.uuid4()) for _ in range(len(http_df))]
    http_df['activity_id'] = http_df['id']

    # URL处理
    http_df['domain'] = http_df['url'].apply(lambda x: urlparse(x).netloc)
    http_df['path'] = http_df['url'].apply(lambda x: urlparse(x).path)
    http_df['query'] = http_df['url'].apply(lambda x: urlparse(x).query)

    # 提取可能的敏感信息
    http_df['contains_sensitive_keywords'] = http_df['url'].str.contains('password|login|admin', case=False)

    # 计算每个用户的访问频率
    http_df['timestamp'] = pd.to_datetime(http_df['date'])
    http_df['visit_frequency'] = http_df.groupby('user')['timestamp'].diff().dt.total_seconds()

    http_details_columns = [
        'http_id', 'activity_id', 'domain', 'path', 'query',
        'contains_sensitive_keywords', 'visit_frequency'
    ]
    http_details_df = http_df[http_details_columns]
    http_details_df.to_csv(output_http_path, index=False)
    print("HTTP details processed and saved successfully.")


def process_file_details():
    file_df = pd.read_csv(file_path)
    file_df['file_id'] = [str(uuid.uuid4()) for _ in range(len(file_df))]
    file_df['activity_id'] = file_df['id']

    # 提取文件扩展名
    file_df['file_extension'] = file_df['filename'].apply(lambda x: os.path.splitext(x)[1].lower())

    # 标记可能的敏感文件类型
    sensitive_extensions = ['.doc', '.pdf', '.xls', '.xlsx', '.zip']
    file_df['is_sensitive_type'] = file_df['file_extension'].isin(sensitive_extensions)

    # 计算文件操作频率
    file_df['timestamp'] = pd.to_datetime(file_df['date'])
    file_df['operation_frequency'] = file_df.groupby('user')['timestamp'].diff().dt.total_seconds()

    file_details_columns = [
        'file_id', 'activity_id', 'filename', 'file_extension',
        'is_sensitive_type', 'operation_frequency'
    ]
    file_details_df = file_df[file_details_columns]
    file_details_df.to_csv(output_file_path, index=False)
    print("File details processed and saved successfully.")


def process_email_details():
    email_df = pd.read_csv(email_path)
    email_df['email_id'] = [str(uuid.uuid4()) for _ in range(len(email_df))]
    email_df['activity_id'] = email_df['id']

    # 提取收件人域名
    email_df['recipient_domain'] = email_df['to'].apply(lambda x: x.split('@')[-1] if '@' in str(x) else '')

    # 检查是否有外部收件人
    email_df['has_external_recipient'] = email_df['recipient_domain'] != 'company.com'  # 替换为实际的公司域名

    # 检查附件
    email_df['has_attachment'] = email_df['attachments'] > 0

    # 计算邮件发送频率
    email_df['timestamp'] = pd.to_datetime(email_df['date'])
    email_df['send_frequency'] = email_df.groupby('user')['timestamp'].diff().dt.total_seconds()

    # 检查邮件大小是否异常
    email_df['is_large_email'] = email_df['size'] > 10000000  # 10MB

    email_details_columns = [
        'email_id', 'activity_id', 'to', 'from', 'size', 'attachments',
        'recipient_domain', 'has_external_recipient', 'has_attachment',
        'send_frequency', 'is_large_email'
    ]
    email_details_df = email_df[email_details_columns]
    email_details_df.to_csv(output_email_path, index=False)
    print("Email details processed and saved successfully.")


def main():
    print("Starting data processing...")
    process_http_details()
    process_file_details()
    process_email_details()
    print("All data processing completed.")


if __name__ == "__main__":
    main()