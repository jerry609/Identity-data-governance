import csv
import hashlib
from datetime import datetime
import os

file_paths = {
    'device': 'D:/Pycharm_pro/demo/pythonProject/data/device.csv',
    'email': 'D:/Pycharm_pro/demo/pythonProject/data/email.csv',
    'file': 'D:/Pycharm_pro/demo/pythonProject/data/file.csv',
    'http': 'D:/Pycharm_pro/demo/pythonProject/data/http.csv',
    'logon': 'D:/Pycharm_pro/demo/pythonProject/data/logon.csv'
}
output_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/activity.csv'


def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()


def parse_datetime(date_string):
    return datetime.strptime(date_string, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


def process_device_csv(input_file, activity_writer):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            activity_id = row['id']
            datetime = parse_datetime(row['date'])
            user_id = row['user']
            pc_id = row['pc']
            activity_type = 'Device'
            action_details = row['activity']

            activity_writer.writerow([activity_id, datetime, user_id, pc_id, 'unknown', 'unknown',
                                      activity_type, action_details, 'Low', activity_id, user_id])


def process_email_csv(input_file, activity_writer):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            activity_id = row['id']
            datetime = parse_datetime(row['date'])
            user_id = row['user']
            pc_id = row['pc']
            activity_type = 'Email'
            action_details = f"Email sent to {row['to']}"

            activity_writer.writerow([activity_id, datetime, user_id, pc_id, 'unknown', 'unknown',
                                      activity_type, action_details, 'Low', activity_id, row['to']])


def process_file_csv(input_file, activity_writer):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            activity_id = row['id']
            datetime = parse_datetime(row['date'])
            user_id = row['user']
            pc_id = row['pc']
            activity_type = 'File'
            action_details = f"File operation: {row['filename']}"

            activity_writer.writerow([activity_id, datetime, user_id, pc_id, 'unknown', 'unknown',
                                      activity_type, action_details, 'Low', activity_id, user_id])


def process_http_csv(input_file, activity_writer):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            activity_id = row['id']
            datetime = parse_datetime(row['date'])
            user_id = row['user']
            pc_id = row['pc']
            activity_type = 'HTTP'
            action_details = f"HTTP access: {row['url']}"

            activity_writer.writerow([activity_id, datetime, user_id, pc_id, 'unknown', 'unknown',
                                      activity_type, action_details, 'Low', activity_id, user_id])


def process_logon_csv(input_file, activity_writer):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            activity_id = row['id']
            datetime = parse_datetime(row['date'])
            user_id = row['user']
            pc_id = row['pc']
            activity_type = 'Logon'
            action_details = row['activity']

            activity_writer.writerow([activity_id, datetime, user_id, pc_id, 'unknown', 'unknown',
                                      activity_type, action_details, 'Low', activity_id, user_id])


def main():
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as outfile:
        activity_writer = csv.writer(outfile)

        # 写入表头
        activity_writer.writerow(['activity_id', 'datetime', 'user_id', 'pc_id', 'device_type', 'location',
                                  'activity_type', 'action_details', 'risk_level', 'correlated_id', 'target_user_id'])

        # 处理每个输入文件
        process_device_csv(file_paths['device'], activity_writer)
        process_email_csv(file_paths['email'], activity_writer)
        process_file_csv(file_paths['file'], activity_writer)
        process_http_csv(file_paths['http'], activity_writer)
        process_logon_csv(file_paths['logon'], activity_writer)


if __name__ == "__main__":
    main()