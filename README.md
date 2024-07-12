# 用户行为数据处理与分析系统

这是一个关于用户行为数据处理与分析系统的综合概述，涉及系统的主要特性、架构、数据表设计，以及功能实现。这个系统不仅适用于社交网络数据分析，也可以广泛应用于金融和电商等领域。

## 1. **项目概述**
- **目的**：处理和分析用户行为数据，包括异常行为检测和社交网络分析。
- **数据源**：使用CMU-CERT R4.2版本开源数据集。
- **数据类型**：处理HTTP访问、文件操作、电子邮件活动等多种类型的用户活动数据。

## 2. **系统功能**
- **用户信息管理**：处理组织结构和心理测评数据。
- **用户关系网络分析**：分析和可视化用户间的关系。
- **多类型活动记录和分析**：记录和分析包括电子邮件、文件操作、HTTP访问在内的用户活动。
- **异常行为检测**：为异常行为检测准备和处理特征数据。

## 3. **系统要求**
- **开发环境**：Python 3.7+，pandas 1.0+，MySQL 5.7+ 或其他兼容的关系型数据库。

## 4. **系统架构与数据库设计**
- **模块划分**：用户和组织模块、活动记录模块、交互分析模块。
- **核心数据表**：User、UserRelations、Activity、EmailDetails、FileDetails、HttpDetails、Interaction。
- **数据库结构**：详细设计表格以存储用户信息、活动记录、电子邮件详情等。

## 5. **数据处理流程**
- **数据收集**：从多个源系统收集数据。
- **数据清洗**：处理数据中的缺失值和异常值。
- **数据集成**：整合来自不同来源的数据到统一的数据库中。

## 6. **图分析系统设计**
- **G6图可视化引擎应用**：利用G6进行关系网络的可视化和分析。
- **功能实现**：
  - **关系扩散**：使用递归查询实现多度关系扩散。
  - **关系预判**：基于现有数据，使用机器学习算法预测潜在关系。
  - **关系聚合**：将同类型关系聚合显示，减少视觉干扰。
  - **圈检测**：使用图算法检测和标识闭合关系圈。
  - **圈查询**：查询特定的用户关系圈和成员之间的交互。
  - **高效分析**：实现数据过滤，标记重要节点和边，以及动态显示或隐藏节点和标签。

## 7. **API设计**
- **接口功能**：包括关系扩散、关系预判、数据过滤等。
- **安全措施**：采用HTTPS，实现细粒度访问控制，防止SQL注入。

## 8. **性能优化**
- **数据索引**：为常用查询字段建立索引。
- **数据缓存**：使用Redis缓存常用的图结构数据。
- **按需加载**：对大规模图进行数据分片和按需加载。

## 9. **未来扩展**
- **NLP技术集成**：分析文本内容提取关键信息。
- **时序分析**：研究关系网络随时间的演变。
- **异常检测算法开发**：自动标记可疑交互模式。

## 10. **开源贡献与联系方式**
- **贡献指南**：遵循Fork-and-Pull Request工作流。
- **许可证**：项目采用MIT许可证。
- **联系方式**：项目维护者[@jerry609](https://github.com/jerry609)。

## 其他
## 1. 用户和组织模块

### User表

| 字段名        | 数据类型  | 描述                     |
| ------------- | --------- | ------------------------ |
| user_id       | VARCHAR   | 主键, 用户唯一标识符     |
| employee_name | VARCHAR   | 员工姓名                 |
| email         | VARCHAR   | 员工电子邮件             |
| role          | VARCHAR   | 员工角色                 |
| department    | VARCHAR   | 部门                     |
| team          | VARCHAR   | 团队                     |
| supervisor    | VARCHAR   | 主管的user_id            |
| business_unit | VARCHAR   | 业务单元                 |
| user_type     | VARCHAR   | 用户类型(如员工、销售等) |
| o_score       | FLOAT     | 开放性得分               |
| c_score       | FLOAT     | 尽责性得分               |
| e_score       | FLOAT     | 外向性得分               |
| a_score       | FLOAT     | 宜人性得分               |
| n_score       | FLOAT     | 神经质得分               |
| join_date     | DATE      | 用户加入组织的日期       |
| last_active   | TIMESTAMP | 用户最后活动时间         |

**解释**：
User表是整个系统的核心表，它存储了所有用户的基本信息、组织结构信息以及心理测评结果。这个表合并了原来的DepartmentInfo和Psychometric表的信息，提供了一个统一的用户视图。每个用户都有一个唯一的user_id作为主键。表中包含了用户的个人信息（如姓名、邮箱）、组织信息（如部门、团队、主管）以及心理测评得分。新增的join_date和last_active字段有助于分析用户的活跃度和在职时长。

### UserRelations表

| 字段名        | 数据类型 | 描述                             |
| ------------- | -------- | -------------------------------- |
| relation_id   | VARCHAR  | 主键，关系唯一标识符             |
| user_id_1     | VARCHAR  | 外键，关联到User表               |
| user_id_2     | VARCHAR  | 外键，关联到User表               |
| relation_type | VARCHAR  | 关系类型（如同事、上下级等）     |
| strength      | FLOAT    | 关系强度（可以基于交互频率计算） |

**解释**：
UserRelations表是为了支持社交网络分析而新增的表。它记录了用户之间的各种关系。每个关系都有一个唯一的relation_id作为主键，并通过user_id_1和user_id_2与User表关联。relation_type字段描述了关系的性质，而strength字段量化了关系的强度，这可以基于用户之间的交互频率来计算。

## 2. 活动记录模块

### Activity表

| 字段名         | 数据类型  | 描述                                                   |
| -------------- | --------- | ------------------------------------------------------ |
| activity_id    | VARCHAR   | 主键, 活动唯一标识符                                   |
| datetime       | TIMESTAMP | 事件发生的日期和时间                                   |
| user_id        | VARCHAR   | 外键, 关联到User表                                     |
| pc_id          | VARCHAR   | 计算机ID                                               |
| device_type    | VARCHAR   | 设备类型(如计算机、USB驱动器等)                        |
| location       | VARCHAR   | 活动发生地点                                           |
| activity_type  | VARCHAR   | 活动类型(如登录、设备连接、HTTP访问、文件操作、邮件等) |
| action_details | TEXT      | 活动详情                                               |
| risk_level     | VARCHAR   | 风险等级(高、中、低)                                   |
| correlated_id  | VARCHAR   | 关联ID(用于关联相关活动)                               |
| target_user_id | VARCHAR   | 活动涉及的目标用户（如有）                             |

**解释**：
Activity表记录了系统中所有用户的活动。这个表整合了原来的UserActivity、EmailActivity、FileActivity和HttpActivity表的通用字段。每个活动都有一个唯一的activity_id作为主键，并通过user_id与User表关联。表中记录了活动的基本信息，如发生时间、地点、设备信息等。activity_type字段指明了活动的类型，而action_details字段可以存储更详细的活动信息。risk_level字段有助于快速识别潜在的高风险活动。新增的target_user_id字段用于记录活动涉及的其他用户，这对于社交网络分析很有帮助。

### EmailDetails表

| 字段名             | 数据类型 | 描述                   |
| ------------------ | -------- | ---------------------- |
| email_id           | VARCHAR  | 主键, 邮件唯一标识符   |
| activity_id        | VARCHAR  | 外键, 关联到Activity表 |
| email_to           | TEXT     | 收件人列表             |
| email_from         | VARCHAR  | 发件人                 |
| email_size         | INT      | 电子邮件大小(字节)     |
| email_attachments  | INT      | 附件数量               |
| email_content_hash | VARCHAR  | 邮件内容的哈希值       |

**解释**：
EmailDetails表存储了与邮件活动相关的详细信息。每封邮件都有一个唯一的email_id作为主键，并通过activity_id与Activity表关联。这个表记录了邮件的收发人、大小、附件数量等信息。email_content_hash字段存储了邮件内容的哈希值，这有助于识别重复或类似的邮件，同时保护了邮件的实际内容。

### FileDetails表

| 字段名            | 数据类型 | 描述                   |
| ----------------- | -------- | ---------------------- |
| file_id           | VARCHAR  | 主键, 文件唯一标识符   |
| activity_id       | VARCHAR  | 外键, 关联到Activity表 |
| filename          | VARCHAR  | 文件名                 |
| file_content_hash | VARCHAR  | 文件内容的哈希值       |

**解释**：
FileDetails表存储了与文件操作相关的详细信息。每个文件操作都有一个唯一的file_id作为主键，并通过activity_id与Activity表关联。这个表记录了文件的名称和内容哈希值。使用内容哈希而不是存储实际文件路径可以提高安全性，并且便于检测重复或修改过的文件。

### HttpDetails表

| 字段名           | 数据类型 | 描述                     |
| ---------------- | -------- | ------------------------ |
| http_id          | VARCHAR  | 主键, HTTP访问唯一标识符 |
| activity_id      | VARCHAR  | 外键, 关联到Activity表   |
| url              | TEXT     | 访问的URL                |
| url_content_hash | VARCHAR  | URL内容的哈希值          |

**解释**：
HttpDetails表存储了与HTTP访问相关的详细信息。每次HTTP访问都有一个唯一的http_id作为主键，并通过activity_id与Activity表关联。这个表记录了访问的URL和URL内容的哈希值。url_content_hash字段可以帮助识别重复访问或检测内容变化。

## 3. 交互分析模块

### Interaction表

| 字段名           | 数据类型  | 描述                           |
| ---------------- | --------- | ------------------------------ |
| interaction_id   | VARCHAR   | 主键，交互唯一标识符           |
| from_user_id     | VARCHAR   | 外键，发起交互的用户           |
| to_user_id       | VARCHAR   | 外键，接收交互的用户           |
| activity_id      | VARCHAR   | 外键，关联到Activity表         |
| interaction_type | VARCHAR   | 交互类型（如邮件、文件共享等） |
| timestamp        | TIMESTAMP | 交互发生的时间                 |

**解释**：
Interaction表是为了支持社交网络分析而新增的表。它记录了用户之间的具体交互。每次交互都有一个唯一的interaction_id作为主键。from_user_id和to_user_id字段指明了交互的发起者和接收者，activity_id关联到具体的活动记录。interaction_type描述了交互的类型，这有助于分析不同类型交互的模式和频率。

# 图分析系统设计文档

## 1. 系统概述

本系统旨在利用设计的数据库结构,结合G6图可视化引擎的强大功能,构建一个专注于关系数据展示与分析的重型图分析应用。该系统不仅适用于社交网络数据分析,还可广泛应用于金融、电商等领域。

## 2. 数据库设计

系统的核心数据库设计包括以下主要表格:

1. User表:存储用户基本信息、组织结构信息及心理测评结果
2. UserRelations表:记录用户之间的各种关系
3. Activity表:记录系统中所有用户的活动
4. EmailDetails表:存储邮件活动的详细信息
5. FileDetails表:存储文件操作的详细信息
6. HttpDetails表:存储HTTP访问的详细信息
7. Interaction表:记录用户之间的具体交互

## G6功能实现

### 关系扩散

**实现方式**:
- 利用User表和UserRelations表构建初始关系网络
- 通过递归查询UserRelations表,实现1-6度的关系扩散
- 使用Activity表和Interaction表补充节点间的交互信息

**SQL示例**:
```sql
WITH RECURSIVE relation_tree AS (
  SELECT user_id_1, user_id_2, 1 AS depth
  FROM UserRelations
  WHERE user_id_1 = :start_user_id
  UNION ALL
  SELECT ur.user_id_1, ur.user_id_2, rt.depth + 1
  FROM UserRelations ur
  JOIN relation_tree rt ON ur.user_id_1 = rt.user_id_2
  WHERE rt.depth < 6
)
SELECT DISTINCT u.* 
FROM relation_tree rt
JOIN User u ON rt.user_id_2 = u.user_id
ORDER BY rt.depth;
```

### 关系预判

**实现方式**:
- 基于UserRelations表和Interaction表的数据,使用机器学习算法预测潜在关系
- 在G6图上添加预测边,观察网络变化

**模型训练数据准备示例**:
```sql
SELECT 
  ur.user_id_1, 
  ur.user_id_2, 
  COUNT(i.interaction_id) as interaction_count,
  AVG(DATEDIFF(i.timestamp, LAG(i.timestamp) OVER (PARTITION BY i.from_user_id, i.to_user_id ORDER BY i.timestamp))) as avg_interaction_interval
FROM UserRelations ur
LEFT JOIN Interaction i ON (ur.user_id_1 = i.from_user_id AND ur.user_id_2 = i.to_user_id)
GROUP BY ur.user_id_1, ur.user_id_2;
```

### 关系聚合

**实现方式**:
- 在UserRelations表中添加relation_group字段,用于标识关系组
- 在G6渲染时,首先显示聚合后的关系,点击后展开详细关系

**SQL示例**:
```sql
SELECT 
  user_id_1, 
  user_id_2, 
  GROUP_CONCAT(relation_type) as relation_types,
  COUNT(*) as relation_count
FROM UserRelations
GROUP BY user_id_1, user_id_2, relation_group;
```

### 圈检测

**实现方式**:
- 利用图算法(如Bron–Kerbosch算法)在UserRelations表数据上进行团检测
- 将检测结果存储在新建的UserGroups表中

**表结构示例**:
```sql
CREATE TABLE UserGroups (
  group_id VARCHAR PRIMARY KEY,
  group_members TEXT,
  detection_date TIMESTAMP
);
```

### 圈查询

**实现方式**:
- 基于UserGroups表和UserRelations表,查询特定朋友圈的所有节点及关系

**SQL示例**:
```sql
SELECT ur.*
FROM UserRelations ur
JOIN UserGroups ug ON FIND_IN_SET(ur.user_id_1, ug.group_members) AND FIND_IN_SET(ur.user_id_2, ug.group_members)
WHERE ug.group_id = :group_id;
```

### 3.6 高效分析

#### 数据过滤

**实现方式**:
- 在Activity表中添加importance_level字段
- 根据用户设置的阈值筛选节点和边

**SQL示例**:
```sql
SELECT * FROM Activity
WHERE importance_level >= :threshold
  AND datetime BETWEEN :start_date AND :end_date;
```

#### 标记节点及边

**实现方式**:
- 在User表和UserRelations表中添加is_marked字段
- 在G6渲染时,对标记的节点和边使用特殊样式

#### 隐藏/显示节点

**实现方式**:
- 在User表中添加is_visible字段
- G6渲染时根据is_visible字段决定是否显示节点及相关边


## API设计

1. `/api/graph/expand`: 关系扩散API
2. `/api/graph/predict`: 关系预判API
3. `/api/graph/aggregate`: 关系聚合API
4. `/api/graph/detect-circle`: 圈检测API
5. `/api/graph/query-circle`: 圈查询API
6. `/api/graph/filter`: 数据过滤API
7. `/api/graph/mark`: 标记节点和边API
8. `/api/graph/visibility`: 控制节点可见性API

