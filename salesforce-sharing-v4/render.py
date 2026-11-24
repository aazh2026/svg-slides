"""Reflow the Salesforce diagrams and add evidence-linked explanations."""
import importlib.util
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'salesforce-sharing-v3'
spec = importlib.util.spec_from_file_location('previous_deck', PREVIOUS / 'render.py')
deck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deck)

# Baselines follow the v1.3 planning rubric: three explanations for pages
# with several relationships, four for pages with more exceptions or checks.
EXPLANATIONS = (
    (4, (
        ('权限集组', '将可复用的对象权限按岗位组合。', 1),
        ('记录所有权', '所有者仍需具备对象编辑权限。', 2),
        ('字段表现', '能打开商机的用户仍可能看不到金额。', 1),
        ('对象级特权', 'Modify All 将特权范围限定在指定对象。', 1),
        ('全局特权', 'View All Data 扩展到组织的数据。', 1),
        ('外部许可证', '高容量用户可按账户或联系人关联匹配。', 1),
        ('候选集合', '限制规则对用户已有访问进一步筛选。', 5),
        ('验证建议', '分别用读取、编辑和字段访问验证同条记录。', 1),
    )),
    (4, (
        ('私有基线', '同级用户可通过共享规则等获得例外访问。', 2),
        ('公开只读', '拥有对象编辑权的同事也只获得记录读取权。', 2),
        ('访问级别', '下属只有只读的记录，主管继承后仍为只读。', 2),
        ('继承来源', '角色向上继承覆盖所有权及下属获共享的记录。', 2),
        ('角色建模', '按经理需要查看的数据范围划分角色分支。', 2),
        ('队列持有', '受支持对象的记录可由适格成员领取处理。', 2),
        ('自定义对象', '关闭层级授权会切断此对象的角色继承。', 2),
        ('变更验证', 'OWD 改动后以代表用户复测并记录重算耗时。', 2),
    )),
    (3, (
        ('所有者规则', '改变记录所有者可能改变规则的命中范围。', 3),
        ('条件规则', '用业务字段定义共享范围，接收方单独配置。', 3),
        ('公共组', '多层嵌套会增加成员计算的维护成本。', 3),
        ('团队级别', '同一商机不同成员可获得不同的访问级别。', 3),
        ('手工授权', '可按记录授予指定主体只读或读写访问。', 3),
        ('代码边界', '以外部系统作权威来源时需同步添加与撤销。', 3),
    )),
    (3, (
        ('管理维度', '角色结构按管理访问需求分支。', 2),
        ('销售维度', '区域层级适合矩阵式覆盖和独立汇总。', 4),
        ('独立维护', '启用区域管理后仍需维护角色层级。', 4),
        ('区域成员', '跨业务线支援可按区域子分支建模。', 4),
        ('逐笔授权', '临时售前加入商机团队即可获得该笔访问。', 4),
        ('设计建议', '复用区域覆盖前先确认它已满足协作范围。', 4),
    )),
    (4, (
        ('清理触发', '记录转移所有权时平台清理 Manual 共享。', 3),
        ('残余访问', 'Manual 清除后用户仍可能经其他机制可见。', 3),
        ('代码写入', '使用 Manual 原因的代码记录也随转移清除。', 3),
        ('界面管理', '共享按钮可编辑或删除代码写入的 Manual。', 3),
        ('自定义原因', '其适用范围是自定义对象，可按业务原因维护。', 3),
        ('团队数据', '界面创建团队成员时同时创建成员与共享记录。', 3),
        ('逐笔团队', '每条账户、商机或案例记录只有一个原生团队。', 3),
        ('验证建议', '交接后对照团队名单、共享原因和实际读取权。', 3),
    )),
    (4, (
        ('过滤前提', '限制规则从已有访问中筛选，未授权记录仍不可见。', 5),
        ('对象边界', '限制规则适用于受支持的对象及组织版本。', 5),
        ('界面验证', '同步检查列表、查找、相关列表和报表。', 5),
        ('查询验证', '核对搜索以及 SOQL、SOSL 的返回结果。', 5),
        ('父级授予', '受支持子记录的访问可带出关联账户可见性。', 5),
        ('子级授予', '账户所有者按其角色设置获子记录访问。', 5),
        ('配置粒度', '联系人、商机与案例可分别配置访问级别。', 5),
        ('账户树边界', '访问父账户本身不会带出子账户访问。', 5),
    )),
    (3, (
        ('触发源', '角色、区域、组、规则和所有权变化都可能触发重算。', 6),
        ('变更类型', '成员调整与结构重组的级联范围应分别评估。', 6),
        ('倾斜治理', '超万条的大所有者尽量不设角色，必要时置顶独立分支。', 6),
        ('性能验证', '大体量账户并使用团队或区域时先用沙箱测时。', 6),
        ('延迟机制', '符合条件时由 Salesforce Support 启用延迟重算。', 6),
        ('验收建议', '重算后用代表用户验证授权新增及撤销。', 6),
    )),
    (4, (
        ('对象入口', '先核对许可证、商机读取权和实际用户身份。', 1),
        ('字段分流', '只有金额不可见时优先检查字段级安全。', 1),
        ('层级证据', '对照请求者和当前所有者所在的角色分支。', 7),
        ('规则证据', '核对记录是否命中规则、用户是否属于接收组。', 7),
        ('团队与区域', '同时核对成员身份和记录关联范围。', 7),
        ('交接例外', '所有者刚变更时检查是否清理了 Manual。', 3),
        ('额外过滤', '已获得访问仍不可见时检查适用的限制规则。', 5),
        ('复测建议', '对照应可见与应隔离的用户，查找过度授权。', 7),
    )),
)

# Only the diagram's vertical geometry is reflowed. The insight-red header,
# conclusion and footer are generated at their original positions.
def resize_diagram(group):
    for element in group:
        tag = element.tag.removeprefix('{' + deck.NS + '}')
        for name in ('y', 'y1', 'y2', 'cy'):
            if name in element.attrib:
                y = float(element.get(name))
                element.set(name, f'{118 + (y - 118)*0.772:.3f}')
        if tag == 'rect':
            element.set('height', f"{float(element.get('height'))*0.772:.3f}")
        elif tag == 'polygon':
            points = [coordinate.split(',') for coordinate in element.get('points').split()]
            element.set('points', ' '.join(f'{x},{118 + (float(y)-118)*0.772:.3f}' for x,y in points))
        elif tag == 'circle':
            element.set('r', f"{float(element.get('r'))*0.772:.3f}")
        elif tag == 'text':
            size = float(element.get('font-size'))
            element.set('font-size', f'{max(11, size*0.9):.2f}')

def render_notes(svg, notes):
    svg.rect(48,512,1184,106,'panel','border',7)
    svg.text(62,530,'机制说明与验证要点',13,'blue-deep',True)
    columns = len(notes)//2
    width = 1156/columns
    for i,(title,body,evidence) in enumerate(notes):
        x = 62+(i%columns)*width
        y = 537+(i//columns)*37
        svg.text(x,y+11,title+'  [E'+str(evidence)+']',11,'blue-deep',True,maxw=width-12)
        svg.block(x,y+13,width-12,29,body,11.2)
    return len(notes)

def write_source_map(output, manifest):
    sources = {source['id']: source for source in manifest['sources']}
    lines = ['# 来源与 SVG 映射', '', '| 证据 | 原文定位 | 幻灯片 |', '|---|---|---|']
    for item in manifest['evidence']:
        source = sources[item['source_ids'][0]]
        refs = '、'.join(f"[{page['page']}]({page['file']})"
                        for page in manifest['slides'] if item['id'] in page['evidence_ids'])
        lines.append(f"| {item['id']} · {item['statement']} | [{source['locator']}]({source['url']}) | {refs} |")
    lines += ['', '## 证据边界', ''] + ['- '+line for line in manifest['limitations']]
    lines.append('- 各页新增说明以页内证据 ID 追溯。验证或设计建议按原文机制推导。')
    (output/'source-map.md').write_text('\n'.join(lines)+'\n')


def main():
    manifest = json.loads((PREVIOUS/'slides/manifest.json').read_text())
    results = []
    evidence = {item['id'] for item in manifest['evidence']}
    for page,(draw,layout,entry,settings,(baseline,notes)) in enumerate(
        zip(deck.DRAWINGS,deck.FORMATS,manifest['slides'],deck.PAGES,EXPLANATIONS),1
    ):
        entry['evidence_ids'] = sorted(set(entry['evidence_ids']) | {f'E{n}' for _,_,n in notes})
        assert set(entry['evidence_ids']) <= evidence
        svg = deck.Diagram(entry['title'], settings[3]+'  '+' '.join(f"[{e}]" for e in entry['evidence_ids']),
                           page,manifest['label'])
        root = svg.root
        svg.root = svg.add('g',id='main-visual')
        draw(svg)
        counts = Counter(el.tag.removeprefix('{'+deck.NS+'}') for el in svg.root)
        resize_diagram(svg.root)
        svg.root = root
        actual = render_notes(svg,notes)
        svg.conclusion(settings[-1])
        assert sum(counts.values()) >= 40 and actual == 2*baseline
        report = dict(layout=layout,diagram_elements=sum(counts.values()),
                      note_baseline=baseline,note_target=2*baseline,notes_actual=actual,
                      notes=[dict(title=t,body=b,evidence=f'E{e}') for t,b,e in notes])
        results.append((entry['file'],svg,report))
    out = HERE/'slides'
    out.mkdir(exist_ok=False)
    for name,svg,_ in results:
        svg.write(out/name)
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    write_source_map(out,manifest)
    (out/'visual-qa.json').write_text(json.dumps({name:qa for name,_,qa in results},ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    main()
