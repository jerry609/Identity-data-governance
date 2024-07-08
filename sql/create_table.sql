-- 创建User表
CREATE TABLE User (
    user_id VARCHAR(255) PRIMARY KEY,
    employee_name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(100),
    department VARCHAR(100),
    team VARCHAR(100),
    supervisor VARCHAR(255),
    business_unit VARCHAR(100),
    user_type VARCHAR(50),
    o_score FLOAT,
    c_score FLOAT,
    e_score FLOAT,
    a_score FLOAT,
    n_score FLOAT,
    join_date DATE,
    last_active TIMESTAMP,
    FOREIGN KEY (supervisor) REFERENCES User(user_id)
);

-- 创建UserRelations表
CREATE TABLE UserRelations (
    relation_id VARCHAR(255) PRIMARY KEY,
    user_id_1 VARCHAR(255),
    user_id_2 VARCHAR(255),
    relation_type VARCHAR(50),
    strength FLOAT,
    FOREIGN KEY (user_id_1) REFERENCES User(user_id),
    FOREIGN KEY (user_id_2) REFERENCES User(user_id)
);

-- 创建Activity表
CREATE TABLE Activity (
    activity_id VARCHAR(255) PRIMARY KEY,
    datetime TIMESTAMP,
    user_id VARCHAR(255),
    pc_id VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(255),
    activity_type VARCHAR(50),
    action_details TEXT,
    risk_level VARCHAR(10),
    correlated_id VARCHAR(255),
    target_user_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (target_user_id) REFERENCES User(user_id)
);

-- 创建EmailDetails表
CREATE TABLE EmailDetails (
    email_id VARCHAR(255) PRIMARY KEY,
    activity_id VARCHAR(255),
    email_to TEXT,
    email_from VARCHAR(255),
    email_size INT,
    email_attachments INT,
    email_content_hash VARCHAR(255),
    recipient_domain VARCHAR(255),
    has_external_recipient BOOLEAN,
    send_frequency FLOAT,
    is_large_email BOOLEAN,
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id)
);

-- 创建FileDetails表
CREATE TABLE FileDetails (
    file_id VARCHAR(255) PRIMARY KEY,
    activity_id VARCHAR(255),
    filename VARCHAR(255),
    file_extension VARCHAR(20),
    file_content_hash VARCHAR(255),
    is_sensitive_type BOOLEAN,
    operation_frequency FLOAT,
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id)
);

-- 创建HttpDetails表
CREATE TABLE HttpDetails (
    http_id VARCHAR(255) PRIMARY KEY,
    activity_id VARCHAR(255),
    url TEXT,
    domain VARCHAR(255),
    path TEXT,
    query TEXT,
    url_content_hash VARCHAR(255),
    contains_sensitive_keywords BOOLEAN,
    visit_frequency FLOAT,
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id)
);

-- 创建Interaction表
CREATE TABLE Interaction (
    interaction_id VARCHAR(255) PRIMARY KEY,
    from_user_id VARCHAR(255),
    to_user_id VARCHAR(255),
    activity_id VARCHAR(255),
    interaction_type VARCHAR(50),
    timestamp TIMESTAMP,
    FOREIGN KEY (from_user_id) REFERENCES User(user_id),
    FOREIGN KEY (to_user_id) REFERENCES User(user_id),
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id)
);