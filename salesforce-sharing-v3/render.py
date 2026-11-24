"""Render eight custom Salesforce sharing diagrams with native SVG primitives."""
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / 'insight-red-svg' / 'scripts'))
from svg_core import SVG, C, NS

spec = importlib.util.spec_from_file_location('source_deck', BASE / 'salesforce-sharing-v2' / 'render.py')
source_deck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source_deck)
PAGES = source_deck.PAGES

class Diagram(SVG):
    def label(self, x, y, text, color='blue-deep'):
        self.text(x, y, text, 14, color, True)

    def box(self, x, y, w, h, title, body='', tone='blue'):
        flags = {'blue': ('blue-tint', 'blue-deep'), 'gray': ('panel', 'ink'),
                 'red': ('red-tint', 'red-deep'), 'purple': ('purple-tint', 'purple-deep'),
                 'green': ('green-tint', 'green')}
        fill, ink = flags[tone]
        self.rect(x, y, w, h, fill, 'border', 7)
        self.block(x+12, y+9, w-24, 21, title, 14, ink, True)
        if body:
            self.block(x+12, y+31, w-24, h-31, body, 13, 'ink')

    def line(self, x1, y1, x2, y2, color='blue', dashed=False):
        return self.add('line', x1=x1, y1=y1, x2=x2, y2=y2, stroke=C[color],
                        stroke_width=1.5, stroke_dasharray='5 4' if dashed else None)

    def caption(self, x, y, label, color='secondary'):
        self.text(x, y, label, 12, color)

    def note(self, x, y, w, h, title, body):
        self.card(x, y, w, h, title, body, 'blue-deep')

def access(s):
    s.label(48, 137, '适用完整共享模型时的访问判定')
    s.box(322, 152, 316, 62, '华东商机 · 查看或编辑', '以一名用户发起的操作为例')
    s.arrow(480, 214, 480, 239)
    s.box(322, 239, 316, 67, '对象权限', '用户能对商机执行该操作吗？')
    s.arrow(322, 273, 274, 273, 'title')
    s.caption(280, 262, '否', 'title')
    s.box(48, 239, 226, 67, '对象操作被拒绝', '即使用户是记录所有者', 'red')
    s.arrow(480, 306, 480, 338)
    s.caption(492, 327, '是')
    s.box(322, 338, 316, 70, '记录访问范围', '所有权、OWD、继承或共享是否覆盖？')
    s.arrow(322, 373, 274, 373, 'title')
    s.caption(280, 362, '否', 'title')
    s.box(48, 338, 226, 70, '记录不在访问范围内', '同角色同事仍需授权依据', 'red')
    s.arrow(480, 408, 480, 441)
    s.caption(491, 430, '是')
    s.box(322, 441, 316, 68, '字段级安全', '字段能否查看或编辑？')
    s.arrow(322, 475, 274, 475, 'title')
    s.caption(281, 464, '受限', 'title')
    s.box(48, 441, 226, 68, '字段被隐藏或不可编辑', '记录仍可能可见', 'purple')
    s.arrow(480, 509, 480, 540)
    s.caption(491, 530, '允许')
    s.box(322, 540, 316, 65, '得到可用的记录操作', '同时受对象、记录及字段权限约束', 'green')
    s.label(700, 137, '三项适用边界')
    s.box(700, 176, 532, 90, '高容量外部用户 → 共享集或共享组',
          '角色不适用。按联系人或账户关联配置记录访问。', 'purple')
    s.box(700, 292, 532, 90, '对象级 View All → 绕过记录共享设置',
          '审计用户可查看该对象的记录。全局权限的授权范围更广。')
    s.box(700, 408, 532, 100, '适用限制规则 → 筛选已获访问的记录',
          '记录共享打开候选访问范围。符合条件的用户仍可能被进一步筛选。', 'purple')
    s.caption(700, 575, '图示用于理解权限职责，节点排列表示检查顺序。')

def baseline(s):
    s.label(48, 137, '角色继承树 · 箭头表示已有访问向上继承')
    s.box(277, 160, 290, 70, '销售总监', '从下属角色继承相应访问')
    s.box(76, 291, 284, 72, '华东主管', '继承小林拥有或已获共享的访问')
    s.box(480, 291, 284, 72, '华南主管', '其他分支仍需独立授权')
    for x in (218, 622):
        s.line(x,291,x,260)
    s.line(218,260,622,260)
    s.arrow(422,260,422,230)
    s.caption(440, 248, '管理继承')
    s.box(48, 435, 223, 72, '销售小林', '拥有华东商机 A')
    s.box(292, 435, 223, 72, '同角色同事', '同级无自动授权', 'gray')
    s.box(541, 435, 223, 72, '华南销售', '独立角色分支', 'gray')
    s.line(159,435,159,402); s.line(403,435,403,402); s.line(159,402,403,402)
    s.arrow(218,402,218,363)
    s.line(652,435,652,402); s.line(622,402,652,402); s.arrow(622,402,622,363)
    s.box(48, 550, 223, 57, '商机 A', '所有权')
    s.box(292, 550, 223, 57, '另一条商机 B', '共享给小林 · 只读')
    s.arrow(159,550,159,507)
    s.line(403,550,403,529); s.line(403,529,240,529); s.arrow(240,529,240,507)
    s.label(810, 137, '组织范围默认值 OWD')
    for y,title,body in [
        (160,'Private','跨所有者访问需要单独依据。'),
        (271,'Public Read Only','默认读他人商机。编辑还需记录级写入授权。'),
        (382,'Controlled by Parent','支持的对象根据关联父记录确定访问。'),
        (493,'自定义对象的继承开关','可关闭通过角色层级授权。OWD 变更会触发重算。')]:
        s.box(810,y,422,96,title,body,'gray')

def selection(s):
    s.label(48, 137, '按记录选择方式对照授权机制')
    widths = (226, 216, 226, 240, 276)
    headers = ('业务需求', '记录选择条件', '机制', '接收方', '维护要点')
    rows = [
        ('运营看华东商机','所有者属于华东角色分支','基于所有者的规则','运营公共组','成员变化由公共组管理'),
        ('合规查看指定阶段','商机阶段命中配置条件','基于条件的规则','合规公共组','覆盖满足条件的记录集合'),
        ('售前介入一笔商机','当前商机','商机团队','指定售前成员','为团队成员设只读或读写'),
        ('代班临时访问','当前记录','手工共享','指定用户、角色或组','所有者转移后重新核对'),
        ('外部系统分配访问','由业务逻辑或外部系统决定','Apex 程序化共享','外部名单中的用户或组','维护共享原因、同步和撤销'),
    ]
    x = 48
    for w,t in zip(widths,headers):
        s.rect(x, 153, w, 41, 'dark')
        s.text(x+12,179,t,14,'white',True)
        x += w
    for i,row in enumerate(rows):
        x=48
        for j,(w,t) in enumerate(zip(widths,row)):
            tint = 'blue-tint' if j == 2 else 'panel' if i % 2 == 0 else 'white'
            s.rect(x,194+i*62,w,62,tint,'border')
            s.block(x+12,200+i*62,w-24,50,t,13,'blue-deep' if j in (0,2) else 'ink',j in (0,2),center=True)
            x += w
    s.box(48,523,564,80,'公共组负责组织接收方',
          '可包含用户、角色、区域和其他组；原文建议嵌套不超过五层。')
    s.box(636,523,596,80,'Apex 用于声明式覆盖不到的授权',
          '适用于复杂动态分配或持续沿用外部授权来源。','purple')

def coverage(s):
    s.label(48,137,'企业销售区域管理 · 两条业务线汇聚到同一账户')
    s.label(972,137,'管理继承与临时协作')
    s.box(48,173,266,85,'零售团队','零售经理与销售代表')
    s.box(48,361,266,85,'再营销团队','再营销经理与销售代表','purple')
    s.box(362,173,254,85,'零售区域分支','汇总本业务线的销售业绩')
    s.box(362,361,254,85,'再营销区域分支','保留独立的区域结构','purple')
    s.arrow(314,216,362,216)
    s.arrow(314,404,362,404,'purple')
    s.caption(319,201,'成员')
    s.caption(319,388,'成员','purple')
    s.box(713,247,220,133,'共用账户 A','两条业务线按各自区域配置获得访问','green')
    s.line(616,216,659,216); s.line(659,216,659,283); s.arrow(659,283,713,283)
    s.line(616,404,659,404,'purple'); s.line(659,404,659,343,'purple')
    s.arrow(659,343,713,343,'purple')
    s.caption(666,271,'区域关联')
    s.caption(666,332,'区域关联','purple')
    s.box(48,509,568,91,'为什么选择区域层级','共享覆盖由两条销售分支决定，案例要求各自维护管理与汇总结构。','gray')
    s.arrow(823,380,823,476)
    s.caption(833,438,'关联商机')
    s.box(713,476,220,83,'账户 A 下的商机','逐笔协作仍可用商机团队')
    s.box(972,166,260,75,'销售主管','沿角色层级继承访问','gray')
    s.box(972,290,260,75,'销售小林','所有或获共享的记录','gray')
    s.arrow(1102,290,1102,241)
    s.caption(1114,269,'向上继承')
    s.box(972,476,260,83,'临时售前顾问','按商机团队成员权限协作','gray')
    s.arrow(972,519,933,519)
    s.caption(951,581,'单笔协作独立配置')

def lifecycle(s):
    s.label(48,137,'交接前 · 小林持有华东商机')
    s.label(742,137,'交接后 · 小周持有华东商机')
    s.box(48,158,484,64,'Salesforce 商机所有者 · 小林','同一条华东商机保留原记录标识')
    s.box(748,158,484,64,'Salesforce 商机所有者 · 小周','记录归属改变，共享原因影响授权结果')
    s.box(557,158,166,64,'转移所有权','变更触发点','purple')
    s.arrow(532,190,557,190)
    s.arrow(723,190,748,190)
    data = [
        ('界面手工共享','代班用户获只读 · RowCause = Manual',
         '原 Manual 共享已清除','用户若仍可见，应核对其他授权路径','red','平台清理'),
        ('程序写入 Manual','方式为代码，原因仍是 Manual',
         '同样清除','界面创建与代码写入遵循同一原因规则','red','同一规则'),
        ('自定义项目记录 · Apex 共享','使用自定义 Apex Sharing Reason',
         '自定义原因的共享可保留','此行以独立自定义对象的所有者转移为例','green','独立语义'),
        ('另查商机团队成员','界面添加时建立成员和关联共享记录',
         '校验成员与共享状态','程序化维护时核对两者，并复测访问','blue','并行验证'),
    ]
    for i,(a,b,c,d,tone,verb) in enumerate(data):
        y=252+i*88
        s.box(48,y,484,69,a,b,'gray')
        s.arrow(548,y+34,732,y+34,'title' if tone=='red' else 'blue')
        s.caption(600,y+24,verb,'title' if tone=='red' else 'secondary')
        s.box(748,y,484,69,c,d,tone)

def visibility(s):
    s.label(48,137,'限制规则 · 从现有授权集合筛选')
    s.label(705,137,'隐式共享 · 账户与标准子记录')
    s.box(48,160,594,68,'已获授权的项目记录','示例中用户可访问华东、华北和华南的三条项目记录','gray')
    for i,t in enumerate(('华东项目','华北项目','华南项目')):
        s.box(48+i*204,253,186,58,t,'已有访问')
        s.arrow(141+i*204,311,141+i*204,345,'purple')
    s.box(48,345,594,68,'限制规则 · 只允许当前用户访问所在区域','当前用户属于华东。每条记录分别匹配条件。','purple')
    for i,(t,desc,tone) in enumerate([
        ('华东项目','匹配 · 仍可见','green'), ('华北项目','不匹配 · 过滤','red'), ('华南项目','不匹配 · 过滤','red')]):
        s.arrow(141+i*204,413,141+i*204,447,'purple')
        s.box(48+i*204,447,186,64,t,desc,tone)
    s.box(48,535,594,63,'验证输出','列表、搜索、报表与查询均需要核对。','gray')
    s.box(705,160,249,79,'具有商机访问的用户','从子记录得到父账户可见性')
    s.box(983,160,249,79,'账户所有者','角色设置允许查看子商机')
    s.arrow(830,239,830,289)
    s.caption(841,270,'父级隐式共享')
    s.arrow(1107,239,1107,289)
    s.caption(1118,270,'子级隐式共享')
    s.box(705,289,249,75,'关联账户 A','账户成为可见记录','green')
    s.box(983,289,249,75,'账户 A 的商机','获得配置范围内的访问','green')
    s.box(705,425,527,119,'父账户 A 与子账户 B',
          '父子账户关系表达结构。账户 B 仍需自己的可见性依据。','gray')
    s.caption(705,584,'隐式共享适用原文列举的标准关系。')

def scale(s):
    s.label(48,137,'批量变更时间线 · 衡量、执行、恢复、复测')
    s.line(182,252,1098,252,'blue')
    phases = [
        ('范围清点','确认变动','角色、区域、组、团队及所有权','得到影响清单','识别级联及依赖'),
        ('沙箱复演','测试分布','单父记录及单所有者记录峰值','取得窗口基线','分别测修改和重算'),
        ('生产变更','集中切换','适用时联系 Support 延迟重算','重新计算共享','集中变更后恢复计算'),
        ('可见性复测','校验结果','覆盖应有访问和意外可见','关闭窗口','记录耗时、异常及结论'),
    ]
    for i,(title,head,detail,outcome,result) in enumerate(phases):
        x=48+306*i
        s.box(x,158,266,74,head,detail)
        s.line(x+133,232,x+133,241)
        s.add('circle',cx=x+133,cy=252,r=9,fill=C['blue'])
        s.caption(x+8,280,f'{i+1:02}  {title}','blue-deep')
        s.arrow(x+133,261,x+133,300)
        s.box(x,300,266,72,outcome,result,'gray')
    s.label(48,416,'原文规模提示与发布计划')
    for x,title,body,tone in [
        (48,'约 1 万条 · 倾斜参考','关注单父记录关联大量子记录，或单一所有者持有大量记录。','red'),
        (452,'超 200 万账户 · 评估共享性能','原文针对企业销售区域管理或团队场景强调关注性能。','red'),
        (856,'共享计算纳入发布验收','将数据修改、重算和可见性复测都计入发布窗口。','blue')]:
        s.box(x,439,376,139,title,body,tone)

def troubleshoot(s):
    s.label(48,137,'排障决策树 · 一名用户、一条记录、一个预期操作')
    s.box(362,151,392,63,'售前反馈华东商机不可见','验证用户身份、预期操作与当前所有者')
    s.arrow(558,214,558,240)
    s.box(362,240,392,65,'有商机读取权限吗？','仅个别字段异常时核对字段级安全')
    s.arrow(362,273,323,273,'title')
    s.caption(332,261,'否','title')
    s.box(48,240,275,65,'修正对象授权','核对许可证和对象权限','red')
    s.arrow(558,305,558,333)
    s.caption(572,324,'是')
    s.box(362,333,392,65,'基线或角色继承覆盖这名用户吗？','核对 OWD 与双方角色分支')
    s.arrow(754,365,806,365)
    s.caption(772,353,'是')
    s.box(806,333,426,65,'核对额外限制','适用时查限制规则和记录匹配条件','purple')
    s.arrow(558,398,558,438)
    s.caption(572,424,'否 → 查预期的横向授权')
    s.line(183,438,1074,438)
    columns = [
      (48,135,'规则或公共组','核对条件、源记录和接收方'),
      (345,135,'团队或区域','核对成员资格、记录归属'),
      (642,135,'手工共享','检查是否因转移所有权清除'),
      (939,135,'程序共享','核对触发条件与实际共享记录'),
    ]
    for x,offset,title,body in columns:
        s.arrow(x+offset,438,x+offset,465)
        s.box(x,465,273,69,title,body,'gray')
    for x in (183,480,777,1074):
        s.line(x,534,x,555)
    s.line(183,555,1074,555)
    s.arrow(558,555,558,568)
    s.box(362,568,392,47,'按同一用户复测并记录命中路径','', 'green')

DRAWINGS = (access, baseline, selection, coverage, lifecycle, visibility, scale, troubleshoot)
FORMATS = ('判定流程与并列权限例外', '继承树与基线侧栏', '全宽选型矩阵',
           '双区域汇聚与角色纵线', '双栏前后状态图', '集合筛选与隐式访问双面板',
           '横向发布阶段时间线', '带终止分支的排障决策树')

def main():
    manifest = json.loads((BASE/'salesforce-sharing-v2/slides/manifest.json').read_text())
    results = []
    for page,(draw,style,entry,spec) in enumerate(zip(DRAWINGS,FORMATS,manifest['slides'],PAGES),1):
        svg = Diagram(entry['title'], spec[3]+'  '+' '.join(f"[{e}]" for e in entry['evidence_ids']),
                      page, manifest['label'])
        root = svg.root
        svg.root = svg.add('g', id='main-visual')
        draw(svg)
        counts = Counter(el.tag.removeprefix('{'+NS+'}') for el in svg.root)
        total = sum(counts.values())
        if total < 40:
            raise ValueError((entry['file'],total))
        svg.root = root
        svg.conclusion(spec[-1])
        results.append((entry['file'],svg,dict(format=style, total=total,elements=dict(counts))))
    out = HERE/'slides'
    out.mkdir(exist_ok=False)
    for name,svg,_ in results:
        svg.write(out/name)
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (out/'source-map.md').write_text((BASE/'salesforce-sharing-v2/slides/source-map.md').read_text())
    (out/'visual-qa.json').write_text(json.dumps({name:qa for name,_,qa in results},ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    main()
