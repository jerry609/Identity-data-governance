# 用户行为数据处理与分析系统

## 项目概述

本项目旨在处理和分析用户行为数据，支持异常用户行为检测和社交网络分析。系统处理多种类型的用户活动数据，包括HTTP访问、文件操作、电子邮件活动等，并提供用户关系和交互分析功能。目前使用的是开源数据集CMU-CERT R4.2版本。

## 功能特性

- 用户信息管理，包括组织结构和心理测评数据
- 用户关系网络分析
- 多种类型的用户活动记录和分析
- 电子邮件、文件操作和HTTP访问的详细信息处理
- 用户交互数据生成和分析
- 为异常行为检测准备特征数据

## 系统要求

- Python 3.7+
- pandas 1.0+
- MySQL 5.7+ 或其他兼容的关系型数据库

## 数据库结构

### 1. 用户和组织模块

#### User表

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

#### UserRelations表

| 字段名        | 数据类型 | 描述                             |
| ------------- | -------- | -------------------------------- |
| relation_id   | VARCHAR  | 主键，关系唯一标识符             |
| user_id_1     | VARCHAR  | 外键，关联到User表               |
| user_id_2     | VARCHAR  | 外键，关联到User表               |
| relation_type | VARCHAR  | 关系类型（如同事、上下级等）     |
| strength      | FLOAT    | 关系强度（可以基于交互频率计算） |

### 2. 活动记录模块

#### Activity表

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
| recipient_domain   | VARCHAR  | 收件人域名             |
| has_external_recipient | BOOLEAN | 是否有外部收件人   |
| send_frequency     | FLOAT    | 发送频率               |
| is_large_email     | BOOLEAN  | 是否为大型邮件         |

**解释**：
EmailDetails表存储了与邮件活动相关的详细信息。除了基本的邮件属性外，还添加了一些用于异常检测的字段。recipient_domain和has_external_recipient用于识别潜在的数据泄露风险。send_frequency可以帮助检测异常的邮件发送模式。is_large_email用于标记可能包含敏感信息的大型邮件。

### FileDetails表

| 字段名            | 数据类型 | 描述                   |
| ----------------- | -------- | ---------------------- |
| file_id           | VARCHAR  | 主键, 文件唯一标识符   |
| activity_id       | VARCHAR  | 外键, 关联到Activity表 |
| filename          | VARCHAR  | 文件名                 |
| file_extension    | VARCHAR  | 文件扩展名             |
| file_content_hash | VARCHAR  | 文件内容的哈希值       |
| is_sensitive_type | BOOLEAN  | 是否为敏感文件类型     |
| operation_frequency | FLOAT  | 文件操作频率           |

**解释**：
FileDetails表记录了文件操作的详细信息。新增的file_extension字段有助于识别特定类型的文件操作。is_sensitive_type用于标记可能包含敏感信息的文件类型。operation_frequency可以帮助检测异常的文件操作模式，如频繁的文件访问或修改。

### HttpDetails表

| 字段名                    | 数据类型 | 描述                     |
| ------------------------- | -------- | ------------------------ |
| http_id                   | VARCHAR  | 主键, HTTP访问唯一标识符 |
| activity_id               | VARCHAR  | 外键, 关联到Activity表   |
| url                       | TEXT     | 访问的URL                |
| domain                    | VARCHAR  | URL的域名                |
| path                      | TEXT     | URL的路径                |
| query                     | TEXT     | URL的查询参数            |
| url_content_hash          | VARCHAR  | URL内容的哈希值          |
| contains_sensitive_keywords | BOOLEAN | 是否包含敏感关键词       |
| visit_frequency           | FLOAT    | 访问频率                 |

**解释**：
HttpDetails表存储了与HTTP访问相关的详细信息。新增的domain、path和query字段提供了更细粒度的URL分析能力。contains_sensitive_keywords用于标记可能访问了敏感信息的请求。visit_frequency可以帮助检测异常的网页访问模式，如频繁访问特定网站或反复尝试访问受限资源。

### 3. 交互分析模块

#### Interaction表

| 字段名           | 数据类型  | 描述                           |
| ---------------- | --------- | ------------------------------ |
| interaction_id   | VARCHAR   | 主键，交互唯一标识符           |
| from_user_id     | VARCHAR   | 外键，发起交互的用户           |
| to_user_id       | VARCHAR   | 外键，接收交互的用户           |
| activity_id      | VARCHAR   | 外键，关联到Activity表         |
| interaction_type | VARCHAR   | 交互类型（如邮件、文件共享等） |
| timestamp        | TIMESTAMP | 交互发生的时间                 |

## 使用说明

1. 确保您的原始数据CSV文件位于正确的目录中。
2. 运行数据处理脚本：
3. 处理后的数据将保存在指定的输出目录中。
4. 使用数据库脚本创建必要的表结构：
5. 将处理后的数据导入到相应的数据库表中。

## 数据分析和异常检测

本系统支持多种数据分析和异常检测方法：

1. 用户行为模式分析
2. 社交网络分析
3. 时间序列异常检测
4. 基于规则的异常行为识别

详细的分析方法和异常检测算法请参考项目文档。

## 注意事项

- 请确保在处理和分析数据时遵守相关的数据保护和隐私法规。
- 定期备份数据库以防数据丢失。
- 系统生成的哈希值仅用于示例，生产环境中应使用更安全的哈希算法。

## 贡献指南

欢迎对本项目提出改进建议或直接贡献代码。请遵循标准的Fork-and-Pull Request工作流。项目持续更新中

## 许可证

本项目采用 MIT 许可证 - 详情请见 [LICENSE.md](LICENSE.md) 文件

## 联系方式

项目维护者 - [@jerry609](https://github.com/jerry609)
