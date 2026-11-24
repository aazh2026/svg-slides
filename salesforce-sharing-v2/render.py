"""Build the custom, editable Salesforce sharing diagrams."""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'insight-red-svg' / 'scripts'))
from svg_core import SVG, NS

# Each row captures a distinct path, with the labels naming the relationships.
PAGES = [
    ('access-model', '权限和记录共享共同决定商机可见性', [1, 2, 5],
     '示例｜华东商机由销售小林持有，商机 OWD 为 Private',
     ('主体或入口', '影响访问的条件', '对这条商机的结果'),
     [
         ('所有权', '销售小林|商机所有者', '持有记录', '商机对象允许读写|字段权限允许编辑金额', '权限相符', '可读取并编辑商机|受对象及字段权限约束'),
         ('管理继承', '销售主管|角色在小林上方', '向上继承', '适用角色层级|主管具备商机读取权限', '具备读取权', '可看到这条商机|编辑还需对象权限'),
         ('默认基线', '同角色同事|与小林处于同一角色', '检查默认', 'OWD 为 Private|示例中没有额外共享', '缺少依据', '看不到这条商机|同角色不自动互访'),
         ('对象级特权', '审计人员|需要查看所有商机', '特权覆盖', '商机 View All|对象级权限', '绕过共享', '可查看该商机|读取范围覆盖该对象'),
     ],
     ('许可证先分流', '示意适用于完整共享模型。高容量外部许可证不支持角色，可按账户或联系人关系使用共享集或共享组。'),
     '设计建议｜按用户验证记录、操作和字段三个维度，并单独评审对象级及全局特权。'),
    ('sharing-baseline', 'OWD 决定起点，角色层级把已有访问向上继承', [1, 2],
     '示例｜沿用小林的商机，对比组织默认值和继承设置',
     ('配置或入口', '判断条件', '访问效果'),
     [
         ('私有', '商机 OWD 为 Private|小林仍持有商机', '观察同事', '同事具备商机读写权限|没有额外共享或继承', '仅有基线', '同事看不到商机|小林仍按对象权限操作'),
         ('公开只读', '商机 OWD 为 Public Read Only|小林仍持有商机', '观察同事', '同事具备商机读写权限|使用默认记录访问', '默认读取', '同事可读该商机|编辑需有记录级写入依据'),
         ('上级继承', '小林获得另一条商机的只读共享|记录可由其他用户持有', '沿角色向上', '主管在适用的角色分支上方|具备商机读取权限', '继承等级', '主管也有只读访问|共享所得访问也可继承'),
         ('按父记录控制', '某对象支持 Controlled by Parent|选择该对象作为检查入口', '检查父级', '用户访问关联父记录|有效权限仍约束操作', '随父访问', '子记录范围由父记录访问决定|适用于支持该设置的关系'),
     ],
     ('所有权与继承的边界', '受支持的对象可由队列持有，适格成员可领取。自定义对象可关闭通过角色层级授予访问；改动 OWD 会触发共享重算。'),
     '设计建议｜用同级、上级和跨分支三类用户验证 OWD，再评估更改基线的重算窗口。'),
    ('sharing-selection', '同一条商机可按记录集合、协作成员或业务事件授权', [3, 4],
     '机制选型｜从谁需要访问、需要多少条记录以及授权何时变更出发',
     ('业务触发', '机制与接收方', '生成的访问范围'),
     [
         ('按归属批量', '运营组需要华东销售的商机|范围由记录归属决定', '按所有者', '所有者共享规则 → 运营公共组|源范围可用角色分支表达', '批量开放', '覆盖符合所有者范围的记录|公共组承接接收方成员'),
         ('按字段批量', '合规组需要进入特定阶段的商机|范围随字段条件变化', '按字段值', '条件共享规则 → 合规公共组|例如商机阶段满足配置条件', '条件命中', '覆盖所有命中条件的商机|与单条商机协作独立'),
         ('逐笔协作', '小林请售前协助这条商机|只需访问当前记录', '指定成员', '商机团队 → 指定售前|为成员配置只读或读写', '单笔开放', '只授予当前商机的团队访问|角色可描述协作职责'),
         ('动态分配', '外部系统维护动态授权名单|声明式配置无法表达分配', '事件驱动', 'Apex 写入对象共享记录|跟踪接收方和共享原因', '按代码授予', '覆盖代码明确选中的记录|同步与撤销由实现维护'),
     ],
     ('单笔临时例外', '也可通过手工共享把当前记录授予用户、角色或组。公共组可包含用户、角色、区域及其他组，嵌套宜控制在五层以内。'),
     '设计建议｜先按业务范围匹配声明式机制，再判断其余动态授权是否需要 Apex。'),
    ('sales-coverage', '角色层级与销售区域分别承载管理访问和矩阵覆盖', [2, 4],
     '原文案例改绘｜零售与再营销各自汇总业绩，同时参与同一客户',
     ('参与路径', '控制访问的结构', '访问目标'),
     [
         ('管理纵线', '小林负责的华东商机|小林拥有或获共享访问', '角色关联', '华东销售角色|小林所在的角色', '向上继承', '华东销售主管|沿管理线获得相应访问'),
         ('零售分支', '零售经理与销售代表', '区域成员', '零售区域分支|负责零售业务覆盖与汇总', '区域关联', '共用账户 A|零售业务线获得配置的访问'),
         ('再营销分支', '再营销经理与销售代表', '区域成员', '再营销区域分支|可采用自己的区域结构', '区域关联', '共用账户 A|再营销线获得配置的访问'),
         ('临时售前', '售前顾问', '逐笔加入', '商机团队|只为当前协作配置访问', '单条记录', '账户 A 下的一条商机|按团队成员权限协作'),
     ],
     ('双层级维护', '启用企业销售区域管理后两套层级并行。原文建议需要分别做角色预测和区域预测时，用角色层级表达管理关系，用区域层级表达销售覆盖。'),
     '设计建议｜两套层级分别对齐管理和销售访问需求，避免因结构重复增加共享计算。'),
    ('sharing-lifecycle', '所有者转移会清除 Manual 共享，共享原因决定例外行为', [3],
     '贯穿示例｜小林将华东商机交接给小周，同时检查其他对象的授权实现',
     ('原有授权', '变更或实现方式', '结果与核对点'),
     [
         ('界面手工共享', '小林把当前商机只读共享给代班人|RowCause = Manual', '转移所有权', '小周成为商机所有者|平台清理 Manual 共享', '撤销此路径', '原手工访问消失|代班人仍可能经其他路径访问'),
         ('程序写入 Manual', '代码为该商机写入共享记录|仍使用 Manual 原因', '转移所有权', '小周成为商机所有者|共享生命周期由原因决定', '同类清理', '代码写入的 Manual 同样清除|界面也能管理此类共享'),
         ('自定义共享原因', '自定义对象的项目记录|代码按业务原因写入共享', '转移所有权', '项目记录交接给新所有者|共享原因独立于 Manual', '保留此路径', '自定义原因的共享可继续保留|按业务事件更新或撤销'),
         ('团队成员', '售前是这条商机的团队成员|界面创建成员记录和关联共享', '维护成员', '通过程序创建团队成员|核对成员及关联共享记录', '校验一致性', '团队名单与实际访问一致|同一记录只有一个原生团队'),
     ],
     ('交接验证', '按共享原因核对访问来源。手工共享消失时，仍要检查用户是否经规则、角色继承、区域或其他渠道获得同一记录。'),
     '设计建议｜把所有者转移、临时代班结束和团队成员移除纳入发布前回归测试。'),
    ('visibility-boundaries', '限制规则从已授权集合筛选，账户关联可触发隐式共享', [5],
     '边界对照｜蓝色为获得访问的依据，紫色为过滤条件及结果',
     ('既有条件', '机制或关系', '可见范围的变化'),
     [
         ('规则过滤', '项目人员已获三条项目记录|由默认值与共享机制授予', '评估记录', '限制规则作用于该用户|仅保留其所属区域的记录', '筛选结果', '三条中仅一条匹配时仅可见一条|列表、报表与查询均需验证'),
         ('从子到父', '用户已获该商机的访问|商机关联账户 A', '隐式授予', '原生父级隐式共享|由商机等受支持子对象触发', '父级可见', '用户可看到关联账户 A|账户访问来自子记录关系'),
         ('从父到子', '小林是账户 A 的所有者|其角色配置商机子记录为只读', '检查角色', '原生子级隐式共享|联系人、商机、案例按角色分别配置', '子级可见', '小林可读关联商机|实际操作仍受对象权限约束'),
         ('账户树', '用户能访问父账户 A|账户 B 的父账户是 A', '检查关系', '父子账户关系表达组织结构|本身不触发账户间授权', '独立检查', '账户 B 仍需自身访问依据|例如所有权或显式共享'),
     ],
     ('适用范围', '限制规则仅适用于支持的对象和版本。账户隐式共享由平台自动处理，适用原文列举的标准关系。'),
     '设计建议｜同时用正例和反例检查敏感记录，验证两种方向上的账户关联。'),
    ('scale-recalculation', '批量改组的发布窗口要容纳共享重算', [2, 6],
     '规模化变更｜实施顺序为依据官方指南整理的设计建议',
     ('变更输入', '影响范围或验证动作', '交付条件'),
     [
         ('范围清点', '季度销售区域重组|涉及角色、区域、群组与所有者', '估算影响', '盘点受影响记录与成员关系|区分成员调整和结构重组', '预估级联', '得到重算范围和依赖清单|明确变更负责人'),
         ('沙箱复演', '准备接近生产的数据分布|关注单父记录与单所有者峰值', '测量耗时', '在沙箱执行相同批次|分别观察变更与共享重算', '设定窗口', '取得重算基线|为生产切换留出时间'),
         ('生产切换', '高体量且需集中变更多项配置|评估重复触发自动重算', '协调支持', '联系 Salesforce Support|适用时启用延迟共享计算', '控制批次', '先执行集中变更|完成后恢复并运行共享计算'),
         ('验收关闭', '重算后抽查目标角色和业务分支|包含应有和不应有的访问', '验证结果', '对照变更前后的访问矩阵|核对异常访问及遗漏', '确认稳定', '实际访问与方案一致后关闭窗口|记录测量值和异常'),
     ],
     ('原文规模提示', '关注约 1 万条级别的父子记录倾斜或所有权倾斜。超过 200 万账户且采用团队或销售区域管理时，原文强调关注共享性能。'),
     '设计建议｜把数据修改、共享重算和可见性复测纳入同一个变更计划。'),
    ('access-troubleshooting', '从对象权限出发，沿预期授权路径定位记录不可见', [1, 2, 3, 5, 7],
     '贯穿示例｜售前原应能看华东商机，转交后反馈无法访问',
     ('排查入口', '检查的事实', '结果或下一步'),
     [
         ('对象与字段', '用售前用户定位这条商机|先区分整条记录与单个字段不可见', '核对权限', '验证许可证与对象读取权限|仅字段异常时检查字段级安全', '基础通过', '检查 OWD、当前所有者及角色|确认预期的授权路径'),
         ('默认与继承', '商机 OWD 为 Private|售前与新所有者处于不同分支', '比对角色', '核对新旧所有者与售前角色|检查是否存在向上继承', '没有继承', '转查横向授权|规则、公用组、团队或区域'),
         ('横向授权', '售前应参与这条商机|已明确预期路径为商机团队', '核对名单', '确认售前仍在该商机团队|检查成员与关联共享的访问级别', '定位差异', '有缺口时修复预期路径|同时核查规则或区域适用范围'),
         ('例外与过滤', '若售前原通过临时 Manual 共享|也需核查适用的过滤和代码共享', '追踪交接', '所有者转移会清理 Manual|适用时另查限制规则和程序共享', '复测结果', '用同一售前账号验证预期访问|用对照账号验证隔离'),
     ],
     ('意外可见的反向排查', '从实际拥有的访问查授权来源，包括对象级或全局强权限、继承、规则、团队、区域以及账户隐式共享。'),
     '设计建议｜每次用一名用户、一条记录和一个预期操作复现，记录最终命中的授权依据。'),
]

def node(svg, x, y, w, h, label, color, fill):
    heading, *body = label.split('|')
    svg.rect(x, y, w, h, fill, 'border', 7)
    svg.text(x + 12, y + (19 if len(body) > 1 else 26),
             heading, 13.5, color, True, maxw=w - 24)
    for i, line in enumerate(body):
        svg.text(x + 12, y + (39 if len(body) > 1 else 46) + i * 17,
                 line, 12, 'ink', maxw=w - 24)

def link(svg, x1, x2, y, label, color):
    svg.text((x1 + x2) / 2, y - 10, label, 11, color, True, 'middle', x2 - x1 + 4)
    svg.arrow(x1, y, x2, y, color)

def draw(page, spec, label):
    slug, title, ids, subtitle, columns, rows, note, recommendation = spec
    svg = SVG(title, subtitle + '  ' + ' '.join(f'[E{i}]' for i in ids), page, label)
    root = svg.root
    chart = svg.add('g', id='main-visual')
    svg.root = chart
    for x, heading in zip((204, 554, 904), columns):
        svg.text(x, 138, heading, 14, 'secondary', True)
    for row, (lane, initial, verb, mechanism, outcome, result) in enumerate(rows):
        y = 151 + row * 92
        color = 'purple' if slug == 'visibility-boundaries' and row == 0 else 'blue'
        fill = 'purple-tint' if color == 'purple' else 'blue-tint'
        svg.text(62, y + 43, lane, 14, color, True, maxw=128)
        svg.add('line', x1=48, y1=y + 81, x2=895 if slug == 'sales-coverage' and row == 1 else 1232, y2=y + 81,
                stroke='#dde1e5', stroke_width=1)
        node(svg, 204, y, 250, 70, initial, 'blue-deep', 'panel')
        link(svg, 463, 545, y + 36, verb, color)
        node(svg, 554, y, 250, 70, mechanism, color, fill)
        link(svg, 813, 895, y + 36, outcome, color)
        if slug == 'sales-coverage' and row in (1, 2):
            if row == 1:
                svg.rect(904, y, 328, 162, 'blue-tint', 'border', 7)
                svg.text(920, y + 34, '共用账户 A', 17, 'blue-deep', True)
                svg.text(920, y + 61, '零售线按区域配置获得访问', 13, 'blue-deep')
                svg.text(920, y + 119, '再营销线按区域配置获得访问', 13, 'blue-deep')
                svg.text(920, y + 143, '各自保留区域结构和汇总', 12, 'secondary')
        elif slug == 'visibility-boundaries' and row == 0:
            svg.rect(904, y, 328, 70, 'purple-tint', 'border', 7)
            svg.text(916, y + 22, '仅返回匹配记录', 13.5, 'purple', True)
            for i, (name, passed) in enumerate((('华东 · 可见', True), ('华北 · 过滤', False), ('华南 · 过滤', False))):
                x = 916 + 100 * i
                svg.rect(x, y + 32, 94, 26, 'white' if passed else 'panel', 'border', 4)
                svg.text(x + 47, y + 50, name, 12, 'purple' if passed else 'secondary', True, 'middle')
        else:
            node(svg, 904, y, 328, 70, result, 'blue-deep', 'panel')
    svg.root = root
    svg.rect(48, 532, 1184, 76, 'panel', 'border', 8)
    svg.text(63, 555, note[0], 14, 'blue-deep', True)
    svg.block(63, 567, 1154, 35, note[1], 13)
    svg.conclusion(recommendation)
    # Lane separators are decorative. The other lines encode relationships.
    count = Counter(element.tag.removeprefix('{' + NS + '}')
                    for element in chart if element.tag != '{' + NS + '}line'
                    or element.get('x1') != '48')
    assert sum(count.values()) >= 40
    return slug, title, ids, svg, dict(count)

def main():
    previous = HERE.parent / 'salesforce-sharing' / 'slides'
    manifest = json.loads((previous / 'manifest.json').read_text())
    output = HERE / 'slides'
    rendered = [draw(page, spec, manifest['label']) for page, spec in enumerate(PAGES, 1)]
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(output)
    output.mkdir(exist_ok=True)
    manifest['slides'] = []
    report = {}
    for page, (slug, title, ids, svg, count) in enumerate(rendered, 1):
        filename = slug + '.svg'
        svg.write(output / filename)
        manifest['slides'].append(dict(file=filename, page=page, title=title,
                                       evidence_ids=[f'E{i}' for i in ids]))
        report[filename] = dict(total=sum(count.values()), elements=count)
    manifest['limitations'].append('小林、小周、账户 A 等为机制示例。规模提示为原文评估口径。')
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    source_map = ['# 来源与 SVG 映射', '', '| 证据 | 原文定位 | 幻灯片 |',
                  '|---|---|---|']
    sources = {item['id']: item for item in manifest['sources']}
    for item in manifest['evidence']:
        source = sources[item['source_ids'][0]]
        pages = '、'.join(str(slide['page']) for slide in manifest['slides']
                          if item['id'] in slide['evidence_ids'])
        source_map.append(f"| {item['id']} · {item['statement']} | [{source['locator']}]({source['url']}) | {pages} |")
    source_map += ['', '## 证据边界', ''] + ['- ' + line for line in manifest['limitations']]
    (output / 'source-map.md').write_text('\n'.join(source_map) + '\n')
    (output / 'visual-qa.json').write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    main()
