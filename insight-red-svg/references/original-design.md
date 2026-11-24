  The insight-red design template — a white-background consulting insight-report

  style distilled from the 30-slide "阿里云AI服务技术洞察20261120-汇报v1.1"

  deck (云栖大会技术洞察/管理层汇报). The signature is a dark-red (#C00000)

  judgment title with a thin red rule, a gray subtitle line, and a full-width

  evidence zone. Ink is #24292F (not pure black); the technical accent is

  #0070C0 blue; #6B5B95 purple marks a third category or a "new in 2.0" state;

  #303338 dark-gray table headers; light gray #F6F7F8 panels; pink #FFF1F2 /

  #FCEFF0 tint for conclusions and "new" states. Layout is deliberately

  flexible — full-width architecture, 2/3-column cards, a left diagram with a

  right reading column, and dense tables all appear in the source. The spine

  rule: the title states the page's judgment, evidence is organized into

  labeled cards/rows, and a red conclusion or "启示：" band closes the page.

  Every page carries a page number and a short deck label in the footer; the

  source's corporate logo is NOT part of the template.

  To use: copy this file to a deck's slides dir as design.md and tweak per deck.

  The validator (.claude/skills/svg-slide-validate/validate_deck.py) checks every

  slide's inline SVG literals against the tokens declared here. Only declared

  categories are checked — drop a category if the deck uses none of it.

  Concrete SVG scaffolds (cover/TOC/cards/architecture/table/summary/back-cover)

  using these tokens live in scaffolds.md.

colors:

  # --- page + inks ---

  white: "#ffffff"            # page bg (default), card interiors, table body cells

  ink: "#24292f"              # DEFAULT body text and non-red headings (dark blue-gray)

  ink-2: "#333333"            # secondary body ink for dense cards

  secondary: "#60666d"        # subtitle line, secondary prose, labels

  muted: "#70757c"            # tertiary labels, source notes, table sub-text

  faint: "#8c8c8c"            # footer text, page number, faint captions

  # --- red spine: title + conclusion ---

  title: "#c00000"            # PRIMARY accent — slide title, key emphasis, conclusion, red rule

  red-deep: "#a50009"         # darker red — "new" state chip, strongest emphasis

  red-tint: "#fff1f2"         # pink card fill ("new"/recommended state, right reading panel)

  red-tint-2: "#fceff0"       # lighter pink banner fill (演进主线 / pill tag)

  red-border: "#eebec2"       # pink card border

  # --- technical accents ---

  blue: "#0070c0"             # technical term, metric, link, diagram arrow/flow

  blue-deep: "#002060"        # deep navy for architecture headers / key technical labels

  blue-2: "#30699b"           # secondary blue — table row accent, second category

  blue-tint: "#eff5fb"        # light-blue card/row fill

  purple: "#6b5b95"           # third category — capability domain, "2.0" evolution

  purple-deep: "#2d1b4e"      # deep purple — category header / emphasis

  purple-tint: "#f3f0fb"      # light-purple card/row fill

  purple-border: "#d5cbf1"    # light-purple border

  green: "#277e58"            # positive / done / green row accent

  green-tint: "#eff7f3"       # green-tinted card/row fill

  gold: "#97701c"             # fourth category / caution / gold row accent

  gold-tint: "#faf7ed"        # gold-tinted card/row fill

  # --- structure ---

  dark: "#303338"             # table header fill, section chip, dark banner

  border: "#dde1e5"           # primary card/table border

  border-2: "#dadde1"         # secondary card border

  panel: "#f6f7f8"            # gray card fill (evidence cards, zebra rows)

  panel-2: "#f4f5f7"          # alternate gray panel fill

  row-label: "#edeff1"        # row-label block / legend chip fill

typography:

  # --- single sans spine: 微软雅黑 ---

  title:            { fontFamily: "微软雅黑", fontSize: "28", fontWeight: 700 }      # page title (red)

  title-sm:         { fontFamily: "微软雅黑", fontSize: "24", fontWeight: 700 }      # dense-page title (red)

  subtitle:         { fontFamily: "微软雅黑", fontSize: "13.33" }                     # gray subtitle under the title

  section:          { fontFamily: "微软雅黑", fontSize: "16", fontWeight: 700 }      # section heading inside content

  body:             { fontFamily: "微软雅黑", fontSize: "12" }                       # default body / bullet

  body-lg:          { fontFamily: "微软雅黑", fontSize: "14" }                       # lead sentence / large body

  body-sm:          { fontFamily: "微软雅黑", fontSize: "10.67" }                    # card body / table sub-text

  caption:          { fontFamily: "微软雅黑", fontSize: "9.33" }                     # source note / footnote

  micro:            { fontFamily: "微软雅黑", fontSize: "8.4" }                      # chip / badge text

  card-title:       { fontFamily: "微软雅黑", fontSize: "14.67", fontWeight: 700 }   # card heading

  card-body:        { fontFamily: "微软雅黑", fontSize: "12" }                       # card body

  card-note:        { fontFamily: "微软雅黑", fontSize: "10.67" }                    # card conclusion / note

  table-header:     { fontFamily: "微软雅黑", fontSize: "12", fontWeight: 700 }      # dark table header (white)

  table-body:       { fontFamily: "微软雅黑", fontSize: "11" }                       # table cell

  chip:             { fontFamily: "微软雅黑", fontSize: "10.67" }                    # pill / state chip

  badge:            { fontFamily: "微软雅黑", fontSize: "10.67", fontWeight: 700 }    # numbered badge

  metric:           { fontFamily: "微软雅黑", fontSize: "23", fontWeight: 700 }      # inline metric / number

  metric-lg:        { fontFamily: "微软雅黑", fontSize: "32", fontWeight: 700 }      # hero number

  conclusion:       { fontFamily: "微软雅黑", fontSize: "14", fontWeight: 700 }      # red conclusion line

  cover-title:      { fontFamily: "微软雅黑", fontSize: "32", fontWeight: 700 }

  cover-subtitle:   { fontFamily: "微软雅黑", fontSize: "16", fontWeight: 700 }

  cover-tagline:    { fontFamily: "微软雅黑", fontSize: "14" }

  cover-note:       { fontFamily: "微软雅黑", fontSize: "11" }

  toc-num:          { fontFamily: "微软雅黑", fontSize: "20", fontWeight: 700 }

  toc-title:        { fontFamily: "微软雅黑", fontSize: "16", fontWeight: 700 }

  toc-desc:         { fontFamily: "微软雅黑", fontSize: "12" }

  footer:           { fontFamily: "微软雅黑", fontSize: "9.33" }

rounded:

  xs: 2     # accent strips / thin rules

  sm: 4     # badges / chips

  md: 8     # cards / panels

  pill: 14  # pill tags / state badges

layout:

  canvas: { width: 1280, height: 720 }

  margin: { left: 48, right: 48 }

  content_width: 1184

  header:

    title_y: 64           # title baseline (28px)

    subtitle_y: 86        # subtitle baseline (13.33px)

    rule_y: 98            # red rule top

    rule_height: 4

  content: { y: 118, height: 558 }      # content zone ends y≈676

  footer: { y: 700 }                    # page number left / deck label right (9.33px)

  # optional column zones inside content

  left: { x: 48, width: 748 }           # left diagram / evidence column

  right: { x: 820, width: 412 }         # right reading column (gap ≈24)

  card_3col: { width: 376, gap: 28 }    # x = 48 / 452 / 856

  card_2col: { width: 578, gap: 28 }    # x = 48 / 654

components:

  page-title:     { typography: "{typography.title}", fill: "{colors.title}" }

  page-subtitle:  { typography: "{typography.subtitle}", fill: "{colors.secondary}" }

  title-rule:     { fill: "{colors.title}", height: 4 }

  card:           { fill: "{colors.panel}", stroke: "{colors.border}", rounded: "{rounded.md}" }

  card-accent:    { fill: "{colors.title}", width: 3.2 }

  section-chip:   { fill: "{colors.dark}", typography: "{typography.chip}", text-fill: "{colors.white}" }

  table-header:   { fill: "{colors.dark}", typography: "{typography.table-header}", text-fill: "{colors.white}" }

  tint-banner:    { fill: "{colors.red-tint-2}", typography: "{typography.body}", text-fill: "{colors.title}" }

  conclusion:     { typography: "{typography.conclusion}", fill: "{colors.title}" }

  footer:         { typography: "{typography.footer}", fill: "{colors.faint}" }

\---



**# insight-red design template**



This file is the **\*\*canonical source of truth\*\*** for the insight-red design's

tokens. SKILL.md is design-agnostic (structure/rules/workflow only); this

template + \`scaffolds.md\` carry the concrete design. The structural anatomy of

each slide type lives in SKILL.md; the concrete SVG with these tokens as

literals lives in \`scaffolds.md\` — copy a scaffold, fill in real content, keep

the tokens.



**## Origin: a consulting insight report, not an ops briefing**



The source is a 30-slide 云栖大会技术洞察汇报. It reads as a \*\*consulting

insight report\*\*: a white page, a dark-red \`#C00000\` judgment title, a gray

subtitle line, a thin red rule, then full-width evidence — architecture

diagrams, 3-column cards, dense tables, and a red conclusion / \`启示：\` band.

There is no navy header band (gartner-navy), no 70/30 mandatory split

(huawei-red), and no monochrome notebook medium (ink-\*). The page is a

**\*\*decision memo with diagrams\*\***: red says "this is the judgment", blue says

"this is the technology", purple says "this is the third category / the new

state", and gray carries evidence.



Four things define the template:



1\. **\*\*The red title stack\*\*** — title (\`28px\`, \`#C00000\`, bold) at \`x=48\`,

   baseline \`y=64\`; a gray subtitle (\`13.33px\`, \`#60666D\`) at \`y=86\`; a red

   rule (\`4px\`, \`#C00000\`) at \`y=98\`. The rule spans the content width

   (\`x=48 → 1232\`). The title is a judgment, not a topic label.

2\. **\*\*Full-width evidence\*\*** — content starts at \`y≈118\` and runs to \`y≈676\`.

   The layout is chosen per page: full-width architecture, 2/3-column cards,

   a left diagram (\`w=748\`) + right reading column (\`w=412\`), or a dense table.

   There is no mandatory 70/30 split; the source uses all of these.

3\. **\*\*Labeled cards and colored rows\*\*** — evidence sits in light-gray cards

   (\`#F6F7F8\` + \`#DDE1E5\` border, \`rx=8\`) with a \`3.2px\` red left accent bar

   and a bold card title; tables use a dark \`#303338\` header with white text,

   zebra \`#F6F7F8\`/white rows, and a colored numbered square per row (red /

   blue / green / purple / gold) with a matching tinted first column.

4\. **\*\*The close\*\*** — a red conclusion line (\`14px\`, \`#C00000\`, bold) or a

   \`启示：\` band (pink \`#FCEFF0\` fill, red heading, numbered points) at the

   bottom. The footer carries the page number left and a short deck label

   right (\`9.33px\`, \`#8C8C8C\`); the source's corporate logo is NOT baked in.



**## How tokens relate to the SVG**



The .NET converter reads **\*\*literal inline attrs only\*\*** — it cannot resolve

\`var()\`/\`class\`/\`\<style>\`. So tokens live *\*above\** the SVG: when generating a

slide, write the token's literal value into the attr (\`fill="#c00000"\`, not

\`fill="var(--title)"\`). The validator then checks those literals against this

file. Nothing in this file changes how slides are written — it makes the

already-literal attrs checkable.



**## The red title stack (every content page)**



\`\`\`svg

\<!-- Title (red bold) -->

\<text x="48" y="64" font-family="微软雅黑" font-size="28" font-weight="700" fill="#c00000">AI网关：面向 Agent 的统一流量治理中枢\</text>

\<!-- Subtitle (gray) — omit when the title already carries the full judgment -->

\<text x="48" y="86" font-family="微软雅黑" font-size="13.33" fill="#60666d">传统网关升级为统一控制点：模型接入 · 路由 · 护栏 · 成本 · 可观测\</text>

\<!-- Red rule -->

\<rect x="48" y="98" width="1184" height="4" fill="#c00000"/>

\<!-- Footer -->

\<text x="48" y="700" font-family="微软雅黑" font-size="9.33" fill="#8c8c8c">1\</text>

\<text x="1232" y="700" text-anchor="end" font-family="微软雅黑" font-size="9.33" fill="#8c8c8c">阿里云 AI 服务技术洞察\</text>

\`\`\`



The subtitle is optional — omit it on pages where the title is a complete

judgment and the evidence starts immediately. Never write positional labels

(\`左侧\`/\`右侧\`) or the template name in rendered text.



**## Content zone and layout patterns**



Content starts at \`y≈118\` (below the rule) and ends at \`y≈676\`. The template

supports four evidence layouts; choose the one that matches the content, and

keep the same content type on the same layout across the deck:



\- **\*\*3-column cards\*\*** — \`w=376\`, gap \`28\`, \`x=48 / 452 / 856\`. Each card:

  light-gray fill, thin border, \`3.2px\` red left bar, bold title, 2–4 body

  lines, optional pink conclusion strip.

\- **\*\*2-column cards\*\*** — \`w=578\`, gap \`28\`, \`x=48 / 654\`.

\- **\*\*Left diagram + right reading column\*\*** — left \`x=48 w=748\` (architecture

  or table), right \`x=820 w=412\` (3–5 labeled reading blocks). A red

  conclusion or \`启示：\` band runs full-width beneath.

\- **\*\*Dense table\*\*** — dark \`#303338\` header row, white body rows, zebra

  \`#F6F7F8\` alternate rows, a colored numbered square in the first column,

  and a matching light tint on that column. A red conclusion line sits under

  the table.



Fill the zone: the lowest element lands at \`y∈[640, 676]\`. A page that stops

at \`y≈450\` is unfinished — add a conclusion band or a second evidence row.



**## Color roles**



\- **\*\*Red \`#C00000\`\*\*** — the brand spine: title, red rule, key emphasis inside

  prose, conclusion lines, \`启示：\` heading, numbered section chips. Red is

  the judgment, not decoration; a page carries red in the title + 1–2

  emphasis/conclusion places.

\- **\*\*Deep red \`#A50009\`\*\*** — the strongest state: "2.0 新增" chip, a critical

  change. Use sparingly.

\- **\*\*Blue \`#0070C0\`\*\*** — the technical accent: product/technology names, metrics,

  diagram arrows and flow, links. One or two per page.

\- **\*\*Deep navy \`#002060\` / \`#30699B\`\*\*** — architecture headers, second-level

  boxes, table row accents.

\- **\*\*Purple \`#6B5B95\` / \`#2D1B4E\`\*\*** — the third category, a capability domain,

  the "2.0 evolution" state. Purple is a category color, never a general

  emphasis.

\- **\*\*Green \`#277E58\` / gold \`#97701C\`\*\*** — additional row/category colors in

  dense tables; green also means positive/done.

\- **\*\*Gray \`#F6F7F8\` / \`#F4F5F7\` / \`#EDEFF1\`\*\*** — card and row fills; \`#60666D\`

  / \`#70757C\` / \`#8C8C8C\` are the three text grays (subtitle / tertiary /

  footer).

\- **\*\*Pink tints \`#FFF1F2\` / \`#FCEFF0\`\*\*** — conclusion bands, "new"/recommended

  cards, pill tags. Pink is a *\*tint of red\**, so it belongs to the judgment

  layer, not to arbitrary emphasis.

\- **\*\*Light blue/purple/green/gold tints\*\*** — first-column row tints in a table;

  pair each tint with its solid accent (red→pink, blue→blue-tint,

  purple→purple-tint, green→green-tint, gold→gold-tint).



**## Overrides of SKILL density defaults**



insight-red is a declared override of the SKILL.md "High Information Density"

defaults:



\- **\*\*Title stack replaces the 26px title + insight band\*\*** — the page opens

  with a red title, an optional gray subtitle, and a red rule; there is no

  separate insight band below the title. The title itself is the judgment.

\- **\*\*No mandatory 70/30 split\*\*** — the source uses full-width architecture,

  2/3-column cards, left-diagram/right-notes, and dense tables. Choose per

  content type and stay consistent across pages of the same type.

\- **\*\*Evidence cards, not prose columns\*\*** — the page body is a set of labeled

  cards / table rows / diagram boxes; a wall of prose is off-template.

\- **\*\*Red closes the page\*\*** — the bottom of a content page carries a red

  conclusion line or a \`启示：\` band. Do not end on a gray card with empty

  space below.



The SKILL's structural rules that still apply: one core judgment per slide,

the title states a position (not a topic), cross-slide consistency (same

content type → same pattern), and content-not-form (no positional names or

template geometry in rendered text).



**## Do's and don'ts**



\- **\*\*Do\*\*** open every content page with the red title stack: red title, gray

  subtitle (optional), red rule at \`y=98\`.

\- **\*\*Do\*\*** choose an evidence layout per page: 3-col cards, 2-col cards,

  left diagram + right notes, or a dense table.

\- **\*\*Do\*\*** put the page's judgment in the title and restate it in a red

  conclusion line or \`启示：\` band.

\- **\*\*Do\*\*** use \`3.2px\` red left bars on cards and a colored numbered square in

  table rows.

\- **\*\*Do\*\*** use blue for technology/product/metrics and purple for the third

  category or the "new" state.

\- **\*\*Do\*\*** fill the content zone to \`y≈640–676\` — no large bottom void.

\- **\*\*Do\*\*** use \`微软雅黑\` for all text.

\- **\*\*Do\*\*** carry the footer: page number left, short deck label right, both

  \`9.33px\` \`#8c8c8c\`.

\- **\*\*Don't\*\*** bake a corporate logo or the template name into the page.

\- **\*\*Don't\*\*** use red as a decorative fill across large areas — red is the

  judgment layer (title/rule/conclusion/one emphasis).

\- **\*\*Don't\*\*** use the navy header band from gartner-navy or a mandatory 70/30

  split from huawei-red — this template is white, rule-led, and layout-flexible.

\- **\*\*Don't\*\*** write positional words (\`左侧\`/\`右侧\`) or template geometry as

  rendered text — content only.

\- **\*\*Don't\*\*** use \`var()\`/\`class\` in SVG — inline literals only.

\- **\*\*Don't\*\*** mix font families — \`微软雅黑\` only.