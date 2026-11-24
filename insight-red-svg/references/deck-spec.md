# Deck JSON 输入契约

UTF-8 JSON。参见 examples/deck.json（覆盖五个内置版式）。脚本不联网、不调用模型；Agent 负责输入内容的真实性和结构设计。

顶层：`label` 报告名；`start_page` 起始页码（默认 1）；`sources` 来源数组；`evidence` 证据数组；`limitations` 可选字符串数组；`slides` 页面数组。

- source: `id`（S1…）、`title`、`locator` 必填；`url` 和 `accessed` 可选。官方事实必须提供已访问的 HTTP(S) URL；用户输入 locator 可写“用户输入第 X 段”。
- evidence: `id`（E1…）、`statement`、`kind`（official/user/inference/recommendation）、`source_ids`。推导指向其依据而非虚构来源。
- slide: `id` 英文 slug，`title`，`subtitle`（可选，含事实/建议类别），`layout`，`evidence_ids`，`conclusion`，`data`；architecture/process 可加 `section`、`notes_title` 和 `notes`（1–4 个 `{title,body}`）。
- architecture data: `layers:[{title,nodes:[string,...]}]`，可选 `ordered:true` 明确表示由上至下的顺序；默认不画箭头。
- process data: `steps:[{title,body}]`，自上而下顺序。
- matrix/compare data: `headers:[string]`, `rows:[[string]]`，可选 `weights:[positive number]` 表示相对列宽。compare 使用同一矩阵排版，以维度作为首列。
- cards data: `cards:[{title,body}]`。
- custom SVG：使用原生元素及统一页眉页脚；自行维护与 build.py 一致的 manifest.json 和 source-map.md，运行 validate.py。复杂 path/tspan 需视觉检查。

输出：一页一 SVG；manifest 含 label, sources, evidence, limitations, slides（file,page,title,evidence_ids）；source-map.md 人类可读；qa.json 静态检查结果。来源可追踪不等于事实已验证；Agent 必须查证并在内容中标明推导边界。不要将 JSON 的存在当作验证完成。
