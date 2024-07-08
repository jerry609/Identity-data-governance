import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows系统下SimHei字体路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 加载数据集
user_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\device.csv')
email_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\email.csv')
file_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\file.csv')
http_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\http.csv')
department_info_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\DepartmentInfo.csv')
psychometric_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\psychometric.csv')

# 定义从数据集中提取三元组的函数
def extract_triples(user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df):
    triples = []

    # 从 user_activity_df 提取三元组
    for _, row in user_activity_df.iterrows():
        triples.append((row['UserID'], '进行活动', row['ActivityType']))
        triples.append((row['ActivityType'], '详情', row['ActionDetails']))
        triples.append((row['UserID'], '属于部门', row['Department']))
        triples.append((row['UserID'], '使用设备', row['DeviceType']))
        triples.append((row['UserID'], '在位置', row['Location']))

    # 从 email_activity_df 提取三元组
    for _, row in email_activity_df.iterrows():
        triples.append((row['UserID'], '发送邮件到', row['EmailTo']))
        triples.append((row['UserID'], '使用设备', row['PC']))
        triples.append((row['id'], '邮件大小', row['EmailSize']))
        triples.append((row['id'], '附件数量', row['EmailAttachments']))
        triples.append((row['id'], '邮件内容', row['EmailContentPath']))

    # 从 file_activity_df 提取三元组
    for _, row in file_activity_df.iterrows():
        triples.append((row['UserID'], '访问文件', row['Filename']))
        triples.append((row['Filename'], '文件内容', row['FileContentPath']))

    # 从 http_activity_df 提取三元组
    for _, row in http_activity_df.iterrows():
        triples.append((row['UserID'], '访问网址', row['URL']))
        triples.append((row['URL'], '网址内容', row['URLContentPath']))

    # 从 department_info_df 提取三元组
    for _, row in department_info_df.iterrows():
        triples.append((row['user_id'], '属于部门', row['department']))
        triples.append((row['user_id'], '角色是', row['role']))
        triples.append((row['user_id'], '在业务单元', row['business_unit']))
        triples.append((row['user_id'], '在功能单元', row['functional_unit']))

    # 从 psychometric_df 提取三元组
    for _, row in psychometric_df.iterrows():
        triples.append((row['user_id'], '开放性得分', row['O']))
        triples.append((row['user_id'], '尽责性得分', row['C']))
        triples.append((row['user_id'], '外向性得分', row['E']))
        triples.append((row['user_id'], '宜人性得分', row['A']))
        triples.append((row['user_id'], '神经质得分', row['N']))

    return triples

# 提取三元组
triples = extract_triples(user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df)

# 创建一个有向图
G = nx.DiGraph()

# 添加节点和边
for triple in triples:
    G.add_edge(triple[0], triple[2], label=triple[1])

# 绘制网络图
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20,
        font_family=font_prop.get_name())
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family=font_prop.get_name())

plt.title("三元组网络图", fontproperties=font_prop)
plt.show()
