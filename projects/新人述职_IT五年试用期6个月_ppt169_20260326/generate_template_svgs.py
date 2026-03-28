from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


PROJECT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = PROJECT_DIR / "templates"
OUTPUT_DIR = PROJECT_DIR / "svg_output"


def zh_index(value: int) -> str:
    mapping = {
        1: "一、",
        2: "二、",
        3: "三、",
        4: "四、",
        5: "五、",
        6: "六、",
        7: "七、",
        8: "八、",
        9: "九、",
    }
    return mapping[value]


def text_block(x: int, y: int, lines: list[str], font_size: int = 20, fill: str = "#333F50", weight: str = "400", line_gap: int = 34) -> str:
    parts = [
        f'<text x="{x}" y="{y}" font-family="Microsoft YaHei, Arial, sans-serif" font-size="{font_size}" font-weight="{weight}" fill="{fill}">'
    ]
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_gap
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def bullet_list(x: int, y: int, items: list[str], width: int = 1040, font_size: int = 22, row_gap: int = 46) -> str:
    parts: list[str] = []
    current_y = y
    for item in items:
        parts.append(f'<circle cx="{x}" cy="{current_y - 7}" r="5" fill="#88C100"/>')
        parts.append(text_block(x + 18, current_y, [item], font_size=font_size))
        current_y += row_gap
    return "".join(parts)


def info_card(x: int, y: int, w: int, h: int, title: str, body_lines: list[str], accent: str = "#88C100") -> str:
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="#D8E7B4" stroke-width="1.4"/>',
            f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{accent}"/>',
            text_block(x + 20, y + 34, [title], font_size=20, fill="#6B8E00", weight="700"),
            text_block(x + 20, y + 72, body_lines, font_size=18, fill="#333F50", line_gap=28),
        ]
    )


def metric_card(x: int, y: int, w: int, h: int, label: str, value: str) -> str:
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#F8FBEF" stroke="#CFE1A8" stroke-width="1.2"/>',
            f'<rect x="{x + 16}" y="{y + 16}" width="48" height="48" rx="8" fill="#88C100" fill-opacity="0.14"/>',
            text_block(x + 80, y + 38, [label], font_size=18, fill="#5D6D7E", weight="700"),
            text_block(x + 24, y + 92, [value], font_size=28, fill="#333F50", weight="700"),
        ]
    )


def result_bar(text: str) -> str:
    return "".join(
        [
            '<rect x="56" y="556" width="1168" height="34" rx="8" fill="#F6FBE8" stroke="#CFE1A8" stroke-width="1"/>',
            '<rect x="56" y="556" width="6" height="34" rx="3" fill="#88C100"/>',
            text_block(76, 579, [text], font_size=18, fill="#4F5B66", weight="700", line_gap=24),
        ]
    )


def content_shell(section_index: str, page_title: str, section_name: str, key_message: str, body_svg: str, source: str, note: str, page_num: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <g>
    <rect x="34" y="28" width="44" height="35" fill="#92D050" stroke="#85BB05" stroke-width="1.5"/>
    <rect x="86" y="28" width="8" height="35" fill="#92D050" stroke="#85BB05" stroke-width="1.5"/>
    <line x1="28" y1="76" x2="710" y2="76" stroke="#92D050" stroke-width="3.5"/>
    <line x1="728" y1="76" x2="761" y2="76" stroke="#7F7F7F" stroke-width="3.5"/>
    <line x1="778" y1="76" x2="812" y2="76" stroke="#7F7F7F" stroke-width="3.5"/>
    <text x="1114" y="48" font-family="Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="700" fill="#88C100">RECRUIT</text>
  </g>
  <g>
    <text x="105" y="67" font-family="Microsoft YaHei, Arial, sans-serif" font-size="37" font-weight="400" fill="#333F50">{escape(section_index)}</text>
    <text x="162" y="68" font-family="Microsoft YaHei, Arial, sans-serif" font-size="37" font-weight="700" fill="#333F50">{escape(page_title)}</text>
    <text x="1180" y="67" text-anchor="end" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" font-weight="400" fill="#7F7F7F">{escape(section_name)}</text>
  </g>
  <g>
    <rect x="40" y="102" width="1200" height="52" rx="6" fill="#F6FBE8" stroke="#92D050" stroke-width="1.2"/>
    <rect x="40" y="102" width="6" height="52" rx="3" fill="#88C100"/>
    <text x="62" y="133" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" font-weight="700" fill="#6B8E00">KEY MESSAGE</text>
    <text x="186" y="133" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" font-weight="400" fill="#5D6D7E">{escape(key_message)}</text>
  </g>
  <g>
    <rect x="40" y="176" width="1200" height="430" rx="8" fill="#FFFFFF" stroke="#D8E7B4" stroke-width="1.5"/>
    {body_svg}
  </g>
  <g>
    <rect x="0" y="640" width="1280" height="80" fill="#FAFBFC"/>
    <line x1="0" y1="640" x2="1280" y2="640" stroke="#E5E7EB" stroke-width="1"/>
    <text x="44" y="676" font-family="Microsoft YaHei, Arial, sans-serif" font-size="12" font-weight="400" fill="#7F8C8D">Source: {escape(source)}</text>
    <text x="44" y="700" font-family="Microsoft YaHei, Arial, sans-serif" font-size="11" font-weight="400" fill="#B8C0C2">{escape(note)}</text>
    <rect x="1140" y="654" width="82" height="30" rx="4" fill="#88C100"/>
    <text x="1181" y="675" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">{escape(page_num)}</text>
  </g>
</svg>
'''


def page_03() -> str:
    body = "".join(
        [
            info_card(58, 194, 356, 178, "基础信息", ["华南农业大学 软件工程", "2016 - 2020", "后端开发工程师", "2025-10-20 入职"]) ,
            info_card(434, 194, 370, 178, "职业经历", ["2019 - 2025 深圳乐信控股有限公司", "累计 5 年 IT 行业研发经验", "长期从事会员、活动、运营平台相关研发"]) ,
            info_card(824, 194, 378, 178, "岗位定位", ["当前负责会员、营销活动、运营平台", "快速承接复杂需求并推进方案落地", "兼顾交付效率、系统质量和复用沉淀"]) ,
            '<rect x="58" y="392" width="1144" height="146" rx="12" fill="#F8FBEF" stroke="#CFE1A8" stroke-width="1.2"/>',
            text_block(84, 426, ["核心能力标签"], font_size=20, fill="#6B8E00", weight="700"),
            '<rect x="84" y="448" width="200" height="42" rx="21" fill="#FFFFFF" stroke="#CFE1A8" stroke-width="1"/>',
            text_block(128, 474, ["复杂需求拆解"], font_size=18, weight="700"),
            '<rect x="304" y="448" width="200" height="42" rx="21" fill="#FFFFFF" stroke="#CFE1A8" stroke-width="1"/>',
            text_block(354, 474, ["项目统筹推进"], font_size=18, weight="700"),
            '<rect x="524" y="448" width="200" height="42" rx="21" fill="#FFFFFF" stroke="#CFE1A8" stroke-width="1"/>',
            text_block(574, 474, ["平台化设计"], font_size=18, weight="700"),
            '<rect x="744" y="448" width="200" height="42" rx="21" fill="#FFFFFF" stroke="#CFE1A8" stroke-width="1"/>',
            text_block(794, 474, ["AI 协同研发"], font_size=18, weight="700"),
            '<rect x="964" y="448" width="200" height="42" rx="21" fill="#FFFFFF" stroke="#CFE1A8" stroke-width="1"/>',
            text_block(1002, 474, ["复用机制沉淀"], font_size=18, weight="700"),
            result_bar("具备成熟研发经验，试用期内完成从业务融入到独立承担复杂事项的快速切换。"),
        ]
    )
    return content_shell(zh_index(1), "个人背景与岗位定位", "个人背景与岗位认知", "具备成熟研发经验，入职后快速切入会员、营销活动与运营平台相关业务。", body, "personal_material.md + content_requirement.md", "模板化生成内容页", "03")


def page_04() -> str:
    body = "".join(
        [
            info_card(58, 198, 272, 148, "岗位认知", ["不仅完成开发任务", "也对交付结果、系统质量", "和协作成本负责"]) ,
            info_card(348, 198, 272, 148, "试用期证明", ["无单独绩效承诺书", "以月度绩效结果和交付结果", "作为阶段性证明"]) ,
            info_card(638, 198, 272, 148, "阶段目标", ["尽快熟悉业务并独立承接需求", "在关键项目中承担更大责任"]) ,
            info_card(928, 198, 274, 148, "更高要求", ["把一次性交付沉淀成可复用能力", "成为可放心托付复杂事项的人"]) ,
            '<rect x="58" y="372" width="1144" height="154" rx="12" fill="#FFFFFF" stroke="#D8E7B4" stroke-width="1.4"/>',
            text_block(84, 410, ["试用期工作目标"], font_size=22, fill="#6B8E00", weight="700"),
            bullet_list(88, 450, ["尽快熟悉业务，缩短从理解需求到给出方案的时间", "在关键项目中承担更大责任，兼顾进度、质量与协同效率", "把单次交付沉淀为 SOP、配置化能力和团队经验资产"], font_size=21, row_gap=42),
            result_bar("试用期的核心不是做了多少事，而是能否让团队更放心地把复杂事项交给我。"),
        ]
    )
    return content_shell(zh_index(2), "岗位认知与试用期目标", "岗位认知", "不仅完成开发任务，也对交付结果、系统质量和协作成本负责。", body, "slide_copy_compact.md", "依据模板规范重排为卡片结构", "04")


def page_05() -> str:
    metrics = [
        ("试用期交付", "累计 8 个需求"),
        ("独立负责", "8 个项目 / 事项"),
        ("按期交付率", "100%"),
        ("查询优化", "8s → 500ms"),
        ("节日活动首期", "19 个工作日上线"),
        ("积分提醒覆盖", "40w+ 用户"),
        ("转盘配置化", "1 天 → 2h"),
    ]
    body_parts = []
    positions = [(58, 198), (362, 198), (666, 198), (970, 198), (58, 344), (362, 344), (666, 344)]
    for (label, value), (x, y) in zip(metrics, positions):
        body_parts.append(metric_card(x, y, 272, 118, label, value))
    body_parts.extend(
        [
            '<rect x="970" y="344" width="232" height="118" rx="12" fill="#88C100" fill-opacity="0.08" stroke="#CFE1A8" stroke-width="1.2"/>',
            text_block(992, 378, ["结果覆盖面"], font_size=20, fill="#6B8E00", weight="700"),
            text_block(992, 416, ["交付", "效率", "影响", "复用沉淀"], font_size=22, fill="#333F50", weight="700", line_gap=28),
            result_bar("结果同时覆盖交付、效率、影响和复用价值，整体履职结果达到预期。"),
        ]
    )
    return content_shell(zh_index(3), "6个月整体产出与量化结果", "个人绩效", "工作覆盖交付、优化、系统建设和复用沉淀四个层面。", "".join(body_parts), "slide_copy_compact.md", "指标页按模板卡片规范生成", "05")


def page_06() -> str:
    body = "".join(
        [
            metric_card(58, 198, 216, 104, "项目周期", "2025.11 - 2025.12"),
            metric_card(292, 198, 216, 104, "一期上线", "19 个工作日"),
            metric_card(526, 198, 216, 104, "项目投入", "4 后端 + 3 前端"),
            metric_card(760, 198, 442, 104, "个人角色", "项目负责人 + 核心研发"),
            info_card(58, 324, 270, 192, "Situation", ["时间紧、范围大、协同复杂", "活动分 4 期推进", "需要兼顾拉新、活跃、转化目标"]) ,
            info_card(346, 324, 270, 192, "Task", ["拆解发布节奏", "协调前后端与业务方", "承担关键模块研发与风险兜底"]) ,
            info_card(634, 324, 270, 192, "Action", ["识别核心链路和里程碑", "按期推进联调、提测、上线", "保障每一期可控交付"]) ,
            info_card(922, 324, 280, 192, "Result", ["12.23 完成第四期发布", "在高压项目中稳定交付", "兼顾节奏统筹与研发质量"]) ,
            result_bar("最终按计划完成四期节日活动落地，证明自己不仅能写代码，也能在高压项目中扛结果。"),
        ]
    )
    return content_shell(zh_index(4), "关键案例一｜圣诞与新年活动高压交付", "关键问题突破举例", "在时间紧、范围大、协同复杂的条件下，完成四期活动稳定落地。", body, "slide_copy_compact.md", "案例页采用 STAR 卡片结构", "06")


def page_07() -> str:
    body = "".join(
        [
            '<rect x="58" y="198" width="1144" height="120" rx="12" fill="#F8FBEF" stroke="#CFE1A8" stroke-width="1.2"/>',
            text_block(86, 238, ["从原型、文档到系统实现形成完整闭环，证明独立建设复杂系统的能力。"], font_size=26, fill="#333F50", weight="700"),
            text_block(86, 278, ["系统能力覆盖：调用集、规则链、规则测试执行、多环境管理。"], font_size=20, fill="#5D6D7E"),
            info_card(58, 340, 254, 172, "01 原型", ["自绘原型交互", "在方案阶段提前明确功能边界"]) ,
            info_card(340, 340, 254, 172, "02 文档", ["自编管理台需求文档", "降低协作理解偏差"]) ,
            info_card(622, 340, 254, 172, "03 实现", ["独立实现规则引擎系统", "完成管理台与执行能力建设"]) ,
            info_card(904, 340, 298, 172, "04 价值", ["从承接需求升级为定义方案并独立落地", "形成更强的抽象设计与 ownership 能力"]) ,
            result_bar("从需求接收升级为问题定义、方案设计和独立交付，完成从 0 到 1 的复杂系统建设。"),
        ]
    )
    return content_shell(zh_index(5), "关键案例二｜规则引擎从0到1独立建设", "关键问题突破举例", "从原型、文档到系统实现形成完整闭环，证明独立建设复杂系统的能力。", body, "slide_copy_compact.md", "案例页采用里程碑卡片结构", "07")


def page_08() -> str:
    body = "".join(
        [
            info_card(58, 208, 356, 272, "CRM 查询优化", ["问题：后台查询接口响应慢", "动作：定位瓶颈并重构查询链路", "结果：平均耗时 8s → 500ms", "价值：显著提升运营侧使用效率"]) ,
            info_card(462, 208, 356, 272, "签到重构", ["问题：活动需求重复开发", "动作：抽象为标准配置化能力", "结果：后端无需每次重复开发", "价值：提升需求响应效率和稳定性"]) ,
            info_card(866, 208, 336, 272, "转盘配置化", ["问题：33 个子类问题散落在实现中", "动作：收敛到配置组合", "结果：新增活动由 1 天降到约 2h", "价值：持续降低重复研发成本"]) ,
            result_bar("通过性能优化、架构重构和配置化设计，把一次性交付持续升级为可复用能力。"),
        ]
    )
    return content_shell(zh_index(6), "关键案例三｜优化与平台化建设", "关键问题突破举例", "不只完成需求，更持续把一次性交付升级成可复用能力。", body, "slide_copy_compact.md", "三列平台化案例结构", "08")


def page_09() -> str:
    body = "".join(
        [
            info_card(58, 208, 270, 244, "新人指引", ["编写《后端研发新人指引》", "帮助新同学更快理解环境、流程和协作方式"]) ,
            info_card(346, 208, 270, 244, "工程 SOP", ["梳理新增工程应用 SOP", "梳理上线应用 SOP", "降低重复沟通成本"]) ,
            info_card(634, 208, 270, 244, "AI 协同研发", ["在需求分析、文档整理、代码辅助中实践 AI 方法", "提升信息组织和研发效率"]) ,
            info_card(922, 208, 280, 244, "团队价值", ["将个人经验转化为团队可复用资产", "降低 onboarding 和跨人交接成本"]) ,
            result_bar("在项目交付之外，主动补位团队机制与知识沉淀，让经验可复制、可复用。"),
        ]
    )
    return content_shell(zh_index(7), "个人贡献与方法沉淀", "个人贡献", "在项目交付之外，主动补位团队机制与知识沉淀。", body, "slide_copy_compact.md", "方法沉淀页按四卡片布局生成", "09")


def page_10() -> str:
    rows = [
        ("结果量化不足", "提前定义效果指标", "在项目开始阶段就同步效果口径，避免复盘时只有过程没有结果。"),
        ("业务纵深不足", "系统梳理会员与营销链路", "不只完成模块交付，还进一步补足业务全链路理解。"),
        ("AI 规范沉淀不足", "建设项目级 context 和协作规范", "把个人实践沉淀成团队可复用的方法论和协作约束。"),
    ]
    parts = []
    y = 218
    for title, action, detail in rows:
        parts.extend(
            [
                f'<rect x="58" y="{y}" width="1144" height="96" rx="10" fill="#FFFFFF" stroke="#D8E7B4" stroke-width="1.2"/>',
                f'<rect x="58" y="{y}" width="12" height="96" rx="6" fill="#88C100"/>',
                text_block(92, y + 34, [title], font_size=21, fill="#333F50", weight="700"),
                text_block(390, y + 34, [action], font_size=20, fill="#6B8E00", weight="700"),
                text_block(650, y + 34, [detail], font_size=18, fill="#5D6D7E"),
            ]
        )
        y += 112
    parts.append(result_bar("每个不足都对应明确行动，目标是把改进变成可执行的计划，而不是停留在表态。"))
    return content_shell(zh_index(8), "不足与提升计划", "个人的不足和提升计划", "已识别在量化、业务纵深和团队级规范方面的提升空间。", "".join(parts), "slide_copy_compact.md", "不足页按问题-动作-说明三栏生成", "10")


def page_11() -> str:
    body = "".join(
        [
            info_card(58, 208, 548, 270, "未来 6 个月计划", ["深化 AI 工具使用，继续缩短交付周期", "打造项目级 context，沉淀团队经验", "推进营销活动平台建设，争取 Q2 完成核心能力"]) ,
            info_card(634, 208, 568, 270, "建议与求助", ["为平台化事项预留稳定排期", "提供跨团队协同与数据复盘支持", "帮助关键能力建设获得更持续的资源保障"]) ,
            result_bar("已具备持续承担更大职责的基础，后续会继续围绕 AI 提效、平台建设和经验沉淀三个方向投入。"),
        ]
    )
    return content_shell(zh_index(9), "未来计划、建议与求助", "建议与求助", "未来继续围绕 AI 提效、平台建设和团队经验沉淀三个方向持续投入。", body, "slide_copy_compact.md", "未来计划页按双栏结构生成", "11")


def render_cover() -> str:
    template = (TEMPLATE_DIR / "01_cover.svg").read_text(encoding="utf-8")
    replacements = {
        "{{COVER_TITLE}}": "试用期转正述职报告",
        "{{USERNAME}}": "待补姓名",
        "{{DATE}}": "2026.03.27",
        "{{FORM_CODE}}": "PROBATION-20260327",
        "{{VERSION}}": "v1.0",
    }
    for key, value in replacements.items():
        template = template.replace(key, escape(value))
    return template


def render_toc() -> str:
    return (TEMPLATE_DIR / "02_toc.svg").read_text(encoding="utf-8")


def render_ending() -> str:
    template = (TEMPLATE_DIR / "04_ending.svg").read_text(encoding="utf-8")
    replacements = {
        "{{THANKS_TITLE}}": "THANKS",
        "{{THANKS_SUBTITLE}}": "感谢聆听 | 已在试用期内证明岗位匹配度、结果导向与持续成长潜力",
    }
    for key, value in replacements.items():
        template = template.replace(key, escape(value))
    return template


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pages = {
        "01_cover.svg": render_cover(),
        "02_toc.svg": render_toc(),
        "03_chapter.svg": page_03(),
        "04_role_transition.svg": page_04(),
        "05_6m_kpi.svg": page_05(),
        "06_project_cases.svg": page_06(),
        "07_problem_analysis.svg": page_07(),
        "08_improvement_actions.svg": page_08(),
        "09_next_6m_plan.svg": page_09(),
        "10_risk_support.svg": page_10(),
        "11_value_summary.svg": page_11(),
        "12_ending.svg": render_ending(),
    }
    for filename, content in pages.items():
        (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")
    print(f"Generated {len(pages)} SVG slides in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()