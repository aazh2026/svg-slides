# 来源与 SVG 映射

| 证据 | 原文定位 | 幻灯片 |
|---|---|---|
| E1 · 许可证决定共享模型适用范围。对象权限控制操作，字段权限控制字段可见性和编辑权，记录共享控制可访问的记录。 | [Introduction · High-Volume Users / Profiles and Permission Sets](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [1](access-model.svg)、[2](sharing-baseline.svg)、[8](access-troubleshooting.svg) |
| E2 · 所有权仍受对象权限约束。OWD 定义其他用户记录的默认访问，角色层级在适用时向上继承访问。 | [Record Ownership and Queues / Organization-Wide Defaults / Role Hierarchy](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [1](access-model.svg)、[2](sharing-baseline.svg)、[4](sales-coverage.svg)、[7](scale-recalculation.svg)、[8](access-troubleshooting.svg) |
| E3 · 共享方式可按所有者、字段条件、逐记录协作或代码驱动来选择。手工 RowCause 与自定义 Apex 共享原因的生命周期不同。 | [Public Groups / Sharing Rules / Teams / Manual Sharing / Apex Managed Sharing](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [3](sharing-selection.svg)、[5](sharing-lifecycle.svg)、[8](access-troubleshooting.svg) |
| E4 · 角色层级支持管理访问向上继承，销售区域层级支持矩阵式销售覆盖，记录团队支持单笔协作。 | [Role Hierarchy / Territory Hierarchy / Customer Sharing Solutions](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [3](sharing-selection.svg)、[4](sales-coverage.svg) |
| E5 · 限制规则筛选已获访问的记录。账户有原生隐式共享，账户树本身不传播访问。 | [Restriction Rules / Implicit Sharing / Account Hierarchies’ Impact on Data Access](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [1](access-model.svg)、[6](visibility-boundaries.svg)、[8](access-troubleshooting.svg) |
| E6 · 批量重组要估算级联共享变化。大体量场景应先在沙箱验证，必要时由 Salesforce Support 启用延迟重算。 | [Realignment and Reassignment / Large Data Volumes / Defer Sharing Calculations / Data and Ownership Skews](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [7](scale-recalculation.svg) |
| E7 · 从对象权限和双方角色查起，沿规则和群组、团队或区域、手工及程序共享追踪记录访问。 | [Troubleshooting flow（正文结尾）](https://architect.salesforce.com/docs/architect/fundamentals/guide/platform-sharing-architecture.html) | [8](access-troubleshooting.svg) |

## 证据边界

- 以 Salesforce Architects 原文为依据。示意与实施建议标注在页内。功能支持范围和具体配额应按目标组织验证。
- 小林、小周、账户 A 等为机制示例。规模提示为原文评估口径。
- 各页新增说明以页内证据 ID 追溯。验证或设计建议按原文机制推导。
