# insight-red-svg Agent Skill

面向技术洞察与管理汇报的原生 SVG 生成 Skill。采用 Agent Skills 开放格式（https://agentskills.io/specification）。将本目录完整放入宿主支持的 Skills 目录，不要只复制 SKILL.md；具体发现路径、工具权限和启用方式由宿主决定。

## 使用方式

在支持 Skills 的 Agent 中，例如：
- 使用 insight-red-svg，把这篇官方技术文档 URL 拆成若干页 SVG，保留机制、限制与原文来源，单独列出企业建设启示。
- 使用 insight-red-svg，把下面技术规划转成一页 SVG，接续第 56 页，报告名为技术竞争力规划。
- 批量处理这些链接，交付逐页 SVG、ZIP 和来源映射表。

不依赖宿主的确定性命令示例（在本目录下运行）：

```bash
python3 scripts/build.py examples/deck.json --out ./demo-output
python3 scripts/validate.py ./demo-output --report ./demo-output/qa.json
python3 scripts/preview.py ./demo-output --out ./demo-preview --font 'Noto Sans CJK SC'
python3 scripts/package.py ./demo-output --out ./demo-svg.zip
python3 -m unittest discover -s tests -v
```

核心生成/静态检查/打包均仅依赖 Python 标准库（3.9+）；预览脚本需要环境已有的 CairoSVG 和适用字体，或使用宿主浏览器。预览字体仅影响预览。脚本不联网；URL 研究、事实核对、复杂视觉设计和最终视觉检查由宿主 Agent 执行。

## 验收范围
- 5 种内置语义版式（compare 与 matrix 共用表格布局），复杂图走自定义 SVG。
- 自动静态验证含近似文本尺寸，不保证任意字体实际渲染或图形相交检查，也不验证证据真实性。
- 参考 SVG 来自此前生成的 Salesforce 技术洞察作品，仅用于样式学习；不应复制其内容作为新文档的事实。
- 未在所有 Agent 宿主或 PowerPoint 转换器中进行兼容性验证。
