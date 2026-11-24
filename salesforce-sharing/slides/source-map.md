# 来源与 SVG 映射

| 来源 | 定位 | SVG |
|---|---|---|
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Introduction · High-Volume Users / Profiles and Permission Sets | access-model.svg, access-troubleshooting.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Record Ownership and Queues / Organization-Wide Defaults / Role Hierarchy | access-model.svg, sharing-baseline.svg, sales-coverage.svg, scale-recalculation.svg, access-troubleshooting.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Public Groups / Sharing Rules / Teams / Manual Sharing / Apex Managed Sharing | sharing-selection.svg, sharing-lifecycle.svg, access-troubleshooting.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Role Hierarchy / Territory Hierarchy / Customer Sharing Solutions | sharing-selection.svg, sales-coverage.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Restriction Rules / Implicit Sharing / Account Hierarchies’ Impact on Data Access | access-model.svg, visibility-boundaries.svg, access-troubleshooting.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Realignment and Reassignment / Large Data Volumes / Defer Sharing Calculations / Data and Ownership Skews | scale-recalculation.svg |
| Salesforce Architects · Platform Sharing Architecture https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html | Troubleshooting flow（正文结尾） | access-troubleshooting.svg |

## 证据登记
- E1 (official)：许可证决定共享模型适用范围。对象权限控制操作，字段权限控制字段可见性和编辑权，记录共享控制可访问的记录。 — S1
- E2 (official)：所有权仍受对象权限约束。OWD 定义其他用户记录的默认访问，角色层级在适用时向上继承访问。 — S2
- E3 (official)：共享方式可按所有者、字段条件、逐记录协作或代码驱动来选择。手工 RowCause 与自定义 Apex 共享原因的生命周期不同。 — S3
- E4 (official)：角色层级支持管理访问向上继承，销售区域层级支持矩阵式销售覆盖，记录团队支持单笔协作。 — S4
- E5 (official)：限制规则筛选已获访问的记录。账户有原生隐式共享，账户树本身不传播访问。 — S5
- E6 (official)：批量重组要估算级联共享变化。大体量场景应先在沙箱验证，必要时由 Salesforce Support 启用延迟重算。 — S6
- E7 (official)：从对象权限和双方角色查起，沿规则和群组、团队或区域、手工及程序共享追踪记录访问。 — S7

## 限制
- 以 Salesforce Architects 原文为依据。示意与实施建议标注在页内。功能支持范围和具体配额应按目标组织验证。
