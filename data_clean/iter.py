import pandas as pd
import uuid
from urllib.parse import urlparse
import hashlib
from datetime import datetime

# 文件路径
http_path = 'D:/Pycharm_pro/demo/pythonProject/data/http.csv'
file_path = 'D:/Pycharm_pro/demo/pythonProject/data/file.csv'
email_path = 'D:/Pycharm_pro/demo/pythonProject/data/email.csv'
output_activity_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/activityv2.csv'
output_http_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/http.csv'
output_file_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/file.csv'
output_email_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/email.csv'
output_interaction_path = 'D:/Pycharm_pro/demo/pythonProject/pro_data/interaction.csv'


def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()


def process_activity(http_df, file_df, email_df):
    activities = []

    for df, activity_type in [(http_df, 'http'), (file_df, 'file'), (email_df, 'email')]:
        for _, row in df.iterrows():
            activity = {
                'activity_id': str(uuid.uuid4()),
                'datetime': row['date'],
                'user_id': row['user'],
                'pc_id': row['pc'],
                'device_type': 'unknown',  # 假设设备类型未知
                'location': 'unknown',  # 假设位置未知
                'activity_type': activity_type,
                'action_details': f"{activity_type.capitalize()} activity",
                'risk_level': 'Low',  # 默认风险等级
                'correlated_id': row['id'],
                'target_user_id': row['to'] if activity_type == 'email' else 'unknown'
            }
            activities.append(activity)

    activity_df = pd.DataFrame(activities)
    activity_df.to_csv(output_activity_path, index=False)
    print("Activity data processed and saved successfully.")
    return activity_df


def process_http_details(http_df, activity_df):
    http_details = []
    for _, row in http_df.iterrows():
        activity_id = activity_df[activity_df['correlated_id'] == row['id']]['activity_id'].values[0]
        detail = {
            'http_id': str(uuid.uuid4()),
            'activity_id': activity_id,
            'url': row['url'],
            'url_content_hash': hash_content(row['url'])
        }
        http_details.append(detail)

    http_details_df = pd.DataFrame(http_details)
    http_details_df.to_csv(output_http_path, index=False)
    print("HTTP details processed and saved successfully.")


def process_file_details(file_df, activity_df):
    file_details = []
    for _, row in file_df.iterrows():
        activity_id = activity_df[activity_df['correlated_id'] == row['id']]['activity_id'].values[0]
        detail = {
            'file_id': str(uuid.uuid4()),
            'activity_id': activity_id,
            'filename': row['filename'],
            'file_content_hash': hash_content(row['filename'])  # 实际应用中应该哈希文件内容
        }
        file_details.append(detail)

    file_details_df = pd.DataFrame(file_details)
    file_details_df.to_csv(output_file_path, index=False)
    print("File details processed and saved successfully.")


def process_email_details(email_df, activity_df):
    email_details = []
    for _, row in email_df.iterrows():
        activity_id = activity_df[activity_df['correlated_id'] == row['id']]['activity_id'].values[0]
        detail = {
            'email_id': str(uuid.uuid4()),
            'activity_id': activity_id,
            'email_to': row['to'],
            'email_from': row['from'],
            'email_size': row['size'],
            'email_attachments': row['attachments'],
            'email_content_hash': hash_content(str(row['size']))  # 实际应用中应该哈希邮件内容
        }
        email_details.append(detail)

    email_details_df = pd.DataFrame(email_details)
    email_details_df.to_csv(output_email_path, index=False)
    print("Email details processed and saved successfully.")


def process_interactions(activity_df):
    interactions = []
    for _, row in activity_df.iterrows():
        interaction = {
            'interaction_id': str(uuid.uuid4()),
            'from_user_id': row['user_id'],
            'to_user_id': row['target_user_id'],
            'activity_id': row['activity_id'],
            'interaction_type': row['activity_type'],
            'timestamp': row['datetime']
        }
        interactions.append(interaction)

    interaction_df = pd.DataFrame(interactions)
    interaction_df.to_csv(output_interaction_path, index=False)
    print("Interactions processed and saved successfully.")


def main():
    print("Starting data processing...")

    http_df = pd.read_csv(http_path)
    file_df = pd.read_csv(file_path)
    email_df = pd.read_csv(email_path)

    activity_df = process_activity(http_df, file_df, email_df)
    process_http_details(http_df, activity_df)
    process_file_details(file_df, activity_df)
    process_email_details(email_df, activity_df)
    process_interactions(activity_df)

    print("All data processing completed.")


if __name__ == "__main__":
    main()