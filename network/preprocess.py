import pandas as pd

# Load the datasets from the provided paths
user_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\device.csv')
email_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\email.csv')
file_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\file.csv')
http_activity_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\http.csv')
department_info_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\DepartmentInfo.csv')
psychometric_df = pd.read_csv(r'D:\dataset\cmu-cert r4.2\demo\psychometric.csv')


# Function to check and clean data
def clean_data():
    # Check for missing values and drop or fill them
    user_activity_df.dropna(inplace=True)
    email_activity_df.dropna(inplace=True)
    file_activity_df.dropna(inplace=True)
    http_activity_df.dropna(inplace=True)
    department_info_df.dropna(inplace=True)
    psychometric_df.dropna(inplace=True)

    # Convert date columns to datetime format
    user_activity_df['date'] = pd.to_datetime(user_activity_df['date'])
    email_activity_df['date'] = pd.to_datetime(email_activity_df['date'])
    file_activity_df['date'] = pd.to_datetime(file_activity_df['date'])
    http_activity_df['date'] = pd.to_datetime(http_activity_df['date'])

    # Standardize the column names if necessary
    user_activity_df.columns = map(str.lower, user_activity_df.columns)
    email_activity_df.columns = map(str.lower, email_activity_df.columns)
    file_activity_df.columns = map(str.lower, file_activity_df.columns)
    http_activity_df.columns = map(str.lower, http_activity_df.columns)
    department_info_df.columns = map(str.lower, department_info_df.columns)
    psychometric_df.columns = map(str.lower, psychometric_df.columns)

    return (
    user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df)


# Clean the data
user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df = clean_data()


# Function to find inconsistent user_ids
def find_inconsistent_user_ids(user_activity_df, email_activity_df, file_activity_df, http_activity_df,
                               department_info_df, psychometric_df):
    # Check the integrity of user_id across datasets
    user_ids = set(department_info_df['user_id'])

    inconsistent_user_ids = {
        'user_activity_df': [uid for uid in user_activity_df['user'] if uid not in user_ids],
        'email_activity_df': [uid for uid in email_activity_df['user'] if uid not in user_ids],
        'file_activity_df': [uid for uid in file_activity_df['user'] if uid not in user_ids],
        'http_activity_df': [uid for uid in http_activity_df['user'] if uid not in user_ids],
        'psychometric_df': [uid for uid in psychometric_df['user_id'] if uid not in user_ids],
    }

    return inconsistent_user_ids


# Find inconsistent user_ids
inconsistent_user_ids = find_inconsistent_user_ids(user_activity_df, email_activity_df, file_activity_df,
                                                   http_activity_df, department_info_df, psychometric_df)

# Display the inconsistent user_ids
inconsistent_user_ids_df = pd.DataFrame.from_dict(inconsistent_user_ids, orient='index').transpose()
print("Inconsistent User IDs:")
print(inconsistent_user_ids_df)


# Function to remove inconsistent user_ids
def remove_inconsistent_user_ids(user_activity_df, email_activity_df, file_activity_df, http_activity_df,
                                 department_info_df, psychometric_df):
    user_ids = set(department_info_df['user_id'])

    user_activity_df = user_activity_df[user_activity_df['user'].isin(user_ids)]
    email_activity_df = email_activity_df[email_activity_df['user'].isin(user_ids)]
    file_activity_df = file_activity_df[file_activity_df['user'].isin(user_ids)]
    http_activity_df = http_activity_df[http_activity_df['user'].isin(user_ids)]
    psychometric_df = psychometric_df[psychometric_df['user_id'].isin(user_ids)]

    return (
    user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df)


# Remove inconsistent user_ids
user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df = remove_inconsistent_user_ids(
    user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df, psychometric_df)


# Define function to extract triples
def extract_triples(user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df,
                    psychometric_df):
    triples = []

    # From user_activity_df
    for _, row in user_activity_df.iterrows():
        triples.append((row['user'], '进行活动', row['activity']))
        triples.append((row['activity'], '发生在', row['date']))
        triples.append((row['user'], '使用设备', row['pc']))

    # From email_activity_df
    for _, row in email_activity_df.iterrows():
        triples.append((row['user'], '发送邮件到', row['to']))
        triples.append((row['user'], '使用设备', row['pc']))
        triples.append((row['id'], '邮件大小', row['size']))
        triples.append((row['id'], '附件数量', row['attachments']))
        triples.append((row['id'], '邮件内容', row['content']))

    # From file_activity_df
    for _, row in file_activity_df.iterrows():
        triples.append((row['user'], '访问文件', row['filename']))
        triples.append((row['filename'], '文件内容', row['content']))

    # From http_activity_df
    for _, row in http_activity_df.iterrows():
        triples.append((row['user'], '访问网址', row['url']))
        triples.append((row['url'], '网址内容', row['content']))

    # From department_info_df
    for _, row in department_info_df.iterrows():
        triples.append((row['user_id'], '属于部门', row['department']))
        triples.append((row['user_id'], '角色是', row['role']))
        triples.append((row['user_id'], '在业务单元', row['business_unit']))
        triples.append((row['user_id'], '在功能单元', row['functional_unit']))

    # From psychometric_df
    for _, row in psychometric_df.iterrows():
        triples.append((row['user_id'], '开放性得分', row['o']))
        triples.append((row['user_id'], '尽责性得分', row['c']))
        triples.append((row['user_id'], '外向性得分', row['e']))
        triples.append((row['user_id'], '宜人性得分', row['a']))
        triples.append((row['user_id'], '神经质得分', row['n']))

    return triples


# Extract triples
triples = extract_triples(user_activity_df, email_activity_df, file_activity_df, http_activity_df, department_info_df,
                          psychometric_df)

# Create a directed graph
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Set Chinese font
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows系统下SimHei字体路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for triple in triples:
    G.add_edge(triple[0], triple[2], label=triple[1])

# Simplify the graph by removing less connected nodes
degree_threshold = 2
remove = [node for node, degree in dict(G.degree()).items() if degree <= degree_threshold]
G.remove_nodes_from(remove)

# Draw the network graph
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, k=0.1)  # Adjust k for better spacing
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=8, font_weight="bold", arrowsize=20,
        font_family=font_prop.get_name())
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_family=font_prop.get_name())

plt.title("三元组网络图", fontproperties=font_prop)
plt.show()
