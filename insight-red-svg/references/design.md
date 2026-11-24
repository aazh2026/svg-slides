# Insight-red 视觉契约

基于用户提供的原始 insight-red design（完整备份 original-design.md）与实际 Salesforce SVG 样例。数值由 assets/design-tokens.json 统一管理。默认保持原始视觉风格，不把 Salesforce、公司 logo 或报告页码写死。

- 1280×720，viewBox="0 0 1280 720"，白底。页边距 48；标题 x48 y64，28px 粗体 #c00000（过长可 24px）；副标题 y86 13.33px #60666d；红线 x48 y98 w1184 h4。
- 内容 y118–676。架构/流程可用 x48 w748 与 x820 w412；全幅 w1184；两列 578 / gap28；三列 376 / gap28。底部结论带 y628–676 或按内容安排，色 #fceff0，结论 14px #c00000 粗体。页脚 x48/1232 y700，9.33px #8c8c8c。
- 全部 text 采用 微软雅黑（不转轮廓）；预览时可使用 Noto Sans CJK SC 等兼容字体，不修改交付源。主体通常 12–14px，表格 11–12px，说明 10.67px，来源与页脚 9.33px。标题不能缩到24以下，主体不应小于 10.67px；拆页优先。
- 灰 #f6f7f8 + #dde1e5 描边，rx8；3.2px 红色左强调条。蓝 #0070c0 表示技术与数据流；紫 #6b5b95 表示第三类能力/新状态；红用于判断、风险或门禁，不做大块装饰。表头 #303338 白字，斑马行白/灰，必要时首列配色。
- 内容区尽量落到 y640–676，不用无意义内容填充。采用证据主图而非连续大段文字。标题用自然中文，避免模板词、抽象对仗、形式化标签。
- 来源标识：[E1] 或短来源注，长 URL 收录在 manifest/source-map，不将长链接塞在页内。官方机制、用户输入、洞察、建议、未来规划须在图中可区分。
- 所有视觉属性为 inline literal，不用 style、class、var()、外部资源、图像、脚本。SVG 原生 text、rect、line、path、polygon、circle、ellipse、polyline、g、tspan；复杂 path 需要人工检查。箭头采用线和实心三角形以减少转换器差异。
