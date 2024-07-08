# 用户行为数据处理与分析系统

## 1. 项目概述

本项目旨在处理和分析用户行为数据，支持异常用户行为检测和社交网络分析。系统处理多种类型的用户活动数据，包括HTTP访问、文件操作、电子邮件活动等，并提供用户关系和交互分析功能。目前使用的是开源数据集CMU-CERT R4.2版本。

## 2. 功能特性

- 用户信息管理，包括组织结构和心理测评数据
- 用户关系网络分析
- 多种类型的用户活动记录和分析
- 电子邮件、文件操作和HTTP访问的详细信息处理
- 用户交互数据生成和分析
- 为异常行为检测准备特征数据

## 3. 系统要求

- Python 3.7+
- pandas 1.0+
- MySQL 5.7+ 或其他兼容的关系型数据库
- 。。。（未完待续）

## 4. 系统架构

系统分为三个主要模块：

1. 用户和组织模块
2. 活动记录模块
3. 交互分析模块

### 4.1 数据库结构

#### User表

| 字段名        | 数据类型  | 描述                     |
|---------------|-----------|--------------------------|
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
|---------------|----------|----------------------------------|
| relation_id   | VARCHAR  | 主键，关系唯一标识符             |
| user_id_1     | VARCHAR  | 外键，关联到User表               |
| user_id_2     | VARCHAR  | 外键，关联到User表               |
| relation_type | VARCHAR  | 关系类型（如同事、上下级等）     |
| strength      | FLOAT    | 关系强度（可以基于交互频率计算） |

#### Activity表

| 字段名         | 数据类型  | 描述                                                   |
|----------------|-----------|--------------------------------------------------------|
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

#### EmailDetails表

| 字段名                  | 数据类型 | 描述                   |
|-------------------------|----------|------------------------|
| email_id                | VARCHAR  | 主键, 邮件唯一标识符   |
| activity_id             | VARCHAR  | 外键, 关联到Activity表 |
| email_to                | TEXT     | 收件人列表             |
| email_from              | VARCHAR  | 发件人                 |
| email_size              | INT      | 电子邮件大小(字节)     |
| email_attachments       | INT      | 附件数量               |
| email_content_hash      | VARCHAR  | 邮件内容的哈希值       |
| recipient_domain        | VARCHAR  | 收件人域名             |
| has_external_recipient  | BOOLEAN  | 是否有外部收件人       |
| send_frequency          | FLOAT    | 发送频率               |
| is_large_email          | BOOLEAN  | 是否为大型邮件         |

#### FileDetails表

| 字段名               | 数据类型 | 描述                   |
|----------------------|----------|------------------------|
| file_id              | VARCHAR  | 主键, 文件唯一标识符   |
| activity_id          | VARCHAR  | 外键, 关联到Activity表 |
| filename             | VARCHAR  | 文件名                 |
| file_extension       | VARCHAR  | 文件扩展名             |
| file_content_hash    | VARCHAR  | 文件内容的哈希值       |
| is_sensitive_type    | BOOLEAN  | 是否为敏感文件类型     |
| operation_frequency  | FLOAT    | 文件操作频率           |

#### HttpDetails表

| 字段名                      | 数据类型 | 描述                     |
|-----------------------------|----------|--------------------------|
| http_id                     | VARCHAR  | 主键, HTTP访问唯一标识符 |
| activity_id                 | VARCHAR  | 外键, 关联到Activity表   |
| url                         | TEXT     | 访问的URL                |
| domain                      | VARCHAR  | URL的域名                |
| path                        | TEXT     | URL的路径                |
| query                       | TEXT     | URL的查询参数            |
| url_content_hash            | VARCHAR  | URL内容的哈希值          |
| contains_sensitive_keywords | BOOLEAN  | 是否包含敏感关键词       |
| visit_frequency             | FLOAT    | 访问频率                 |

#### Interaction表

| 字段名           | 数据类型  | 描述                           |
|------------------|-----------|--------------------------------|
| interaction_id   | VARCHAR   | 主键，交互唯一标识符           |
| from_user_id     | VARCHAR   | 外键，发起交互的用户           |
| to_user_id       | VARCHAR   | 外键，接收交互的用户           |
| activity_id      | VARCHAR   | 外键，关联到Activity表         |
| interaction_type | VARCHAR   | 交互类型（如邮件、文件共享等） |
| timestamp        | TIMESTAMP | 交互发生的时间                 |

## 5. 数据处理流程

1. 数据收集：从各种源系统收集原始数据。
2. 数据清洗：处理缺失值、异常值，统一数据格式。
3. 数据集成：将不同来源的数据整合到统一的活动记录中。
4. 特征提取：从原始数据中提取有助于异常检测的特征。
5. 数据存储：将处理后的数据存入相应的数据库表中。

## 6. 异常行为检测

系统支持多种异常行为检测方法：

1. 基于规则的检测：设定阈值和规则，识别违反预定义模式的行为。
2. 统计分析：使用统计方法识别偏离正常分布的行为。
3. 机器学习模型：使用监督或非监督学习算法来检测异常模式。
4. 时间序列分析：检测用户行为随时间变化的异常模式。

## 7. 社交网络分析

利用UserRelations表和Interaction表进行社交网络分析：

1. 关系强度计算：基于交互频率和类型计算用户间的关系强度。
2. 社交图谱构建：可视化用户间的关系网络。
3. 影响力分析：识别网络中的关键节点和影响者。
4. 群体检测：发现和分析用户群体或团队。

## 8. 风险评估

Activity表中的risk_level字段用于快速识别高风险活动：

1. 低风险：正常的日常活动。
2. 中风险：需要关注但不立即危险的活动。
3. 高风险：可能表示严重安全威胁的活动。

## 9. 系统使用指南

1. 数据导入：使用ETL工具或自定义脚本将数据导入各个表中。
2. 数据查询：可以使用SQL查询或专门的分析工具来检索和分析数据。
3. 异常检测：定期运行异常检测算法，识别潜在的异常行为。
4. 报告生成：生成日常活动报告、异常行为报告和社交网络分析报告。

## 10. 安全和隐私

1. 数据加密：确保敏感数据（如邮件内容）使用强加密存储。
2. 访问控制：实施严格的访问控制策略，确保只有授权人员可以访问敏感数据。
3. 数据脱敏：在进行分析时，考虑使用数据脱敏技术保护用户隐私。
4. 审计日志：记录所有对系统的访问和操作，以便追踪和审计。

## 11. 系统维护和优化

1. 定期更新：根据新的安全威胁和用户行为模式更新检测规则和算法。
2. 性能优化：监控查询性能，优化数据库索引和查询语句。
3. 存储管理：实施数据归档和清理策略，管理数据增长。

## 12. 未来扩展

1. 实时分析：引入流处理技术，实现实时异常检测。
2. AI增强：集成更先进的机器学习和深度学习模型。
3. 跨平台集成：扩展系统以包含更多数据源，如移动设备和云服务活动。

## 13. 注意事项

- 请确保在处理和分析数据时遵守相关的数据保护和隐私法规。
- 定期备份数据库以防数据丢失。
- 系统生成的哈希值仅用于示例，生产环境中应使用更安全的哈希算法。

## 14. 贡献指南

欢迎对本项目提出改进建议或直接贡献代码。请遵循标准的Fork-and-Pull Request工作流。项目持续更新中。

## 15. 许可证

本项目采用 MIT 许可证 - 详情请见 [LICENSE.md](LICENSE.md) 文件。

## 16. 联系方式

项目维护者 - [@jerry609](https://github.com/jerry609)
