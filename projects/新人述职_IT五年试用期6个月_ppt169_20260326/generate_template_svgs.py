from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "svg_output"
TEMPLATE_DIR = PROJECT_DIR / "templates"

CANVAS_W = 1280
CANVAS_H = 720

PRIMARY = "#6B8E00"
SECONDARY = "#F6FBE8"
ACCENT = "#88C100"
POSITIVE = "#4D7E2E"
WARNING = "#B9D99E"
TEXT_MAIN = "#2C3E50"
TEXT_SUB = "#5D6D7E"
TEXT_LIGHT = "#94A3B8"
LINE = "#D8E7B4"
BG_LIGHT = "#FAFBFC"

FONT_FAMILY = "Microsoft YaHei, Arial, sans-serif"


CONTENT_AREA_PLACEHOLDER = (
    '<text x="640" y="390" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" '
    'font-size="28" font-weight="400" fill="#AAB7B8">{{CONTENT_AREA}}</text>'
)

CONTENT_GROUP_PLACEHOLDER = (
    '\t<g>\n'
    '\t\t<rect x="40" y="176" width="1200" height="430" rx="8" fill="none" stroke="#D8E7B4" stroke-width="1.5" stroke-dasharray="10 7"/>\n'
    '\t\t<text x="640" y="390" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="28" font-weight="400" fill="#AAB7B8">{{CONTENT_AREA}}</text>\n'
    '\t\t<text x="640" y="424" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" font-weight="400" fill="#C7CFD1">Content Area: 1200 × 430 px</text>\n'
    '\t</g>'
)


def load_template(filename: str) -> str:
    return (TEMPLATE_DIR / filename).read_text(encoding="utf-8")


def replace_tokens(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def render_content_template(
    *,
    title: str,
    takeaway: str,
    body: str,
    page_num: str,
    section_name: str,
    page_index: str,
    source: str,
    note: str,
    replace_full_content_group: bool = False,
) -> str:
    template = load_template("03_content.svg")
    content = replace_tokens(
        template,
        {
            "PAGE_TITLE": escape(title),
            "SECTION_NAME": escape(section_name),
            "KEY_MESSAGE": escape(takeaway),
            "SOURCE": escape(source),
            "NOTE": escape(note),
            "PAGE_NUM": escape(page_num),
        },
    )
    if replace_full_content_group:
        content = content.replace(CONTENT_GROUP_PLACEHOLDER, body)
    else:
        content = content.replace(CONTENT_AREA_PLACEHOLDER, body)
    content = content.replace(
        'font-size="37" font-weight="400" fill="#333F50">一、</text>',
        f'font-size="37" font-weight="400" fill="#333F50">{escape(page_index)}</text>',
        1,
    )
    return content


def svg_page(body: str) -> str:
    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}">',
            body,
            '</svg>',
        ]
    )


def text(x: int, y: int, content: str, size: int = 18, fill: str = TEXT_MAIN, weight: str = "400", anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="{FONT_FAMILY}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(content)}</text>'
    )


def multiline_text(
    x: int,
    y: int,
    lines: list[str],
    size: int = 18,
    fill: str = TEXT_MAIN,
    weight: str = "400",
    line_gap: int = 28,
) -> str:
    parts = [
        f'<text x="{x}" y="{y}" font-family="{FONT_FAMILY}" font-size="{size}" font-weight="{weight}" fill="{fill}">'
    ]
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_gap
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    parts.append('</text>')
    return ''.join(parts)


def pill(x: int, y: int, w: int, h: int, label: str, fill: str = "#FFFFFF", stroke: str = ACCENT, label_fill: str = PRIMARY) -> str:
    return ''.join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>',
            text(x + w // 2, y + h // 2 + 6, label, size=16, fill=label_fill, weight="700", anchor="middle"),
        ]
    )


def metric_card(x: int, y: int, w: int, h: int, label: str, value: str, note: str) -> str:
    return ''.join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.2"/>',
            f'<rect x="{x + 18}" y="{y + 16}" width="48" height="48" rx="10" fill="{SECONDARY}"/>',
            text(x + 84, y + 36, label, size=18, fill=TEXT_SUB, weight="700"),
            text(x + 24, y + 88, value, size=28, fill=TEXT_MAIN, weight="700"),
            text(x + 24, y + 118, note, size=14, fill=ACCENT, weight="700"),
        ]
    )


def info_card(
    x: int,
    y: int,
    w: int,
    h: int,
    title_label: str,
    title_text: str,
    body_lines: list[str],
    accent: str = PRIMARY,
) -> str:
    return ''.join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.2"/>',
            f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{accent}"/>',
            text(x + 20, y + 38, title_label, size=14, fill=accent, weight="700"),
            multiline_text(x + 20, y + 72, [title_text], size=21, fill=TEXT_MAIN, weight="700", line_gap=28),
            multiline_text(x + 20, y + 112, body_lines, size=17, fill=TEXT_SUB, line_gap=26),
        ]
    )


def summary_icon(cx: int, cy: int, kind: str) -> str:
    base = [f'<circle cx="{cx}" cy="{cy}" r="54" fill="{SECONDARY}"/>']
    if kind == "target":
        base.extend(
            [
                f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{PRIMARY}" stroke-width="5"/>',
                f'<circle cx="{cx}" cy="{cy}" r="7" fill="{PRIMARY}"/>',
                f'<line x1="{cx}" y1="{cy - 30}" x2="{cx}" y2="{cy - 16}" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
                f'<line x1="{cx - 20}" y1="{cy + 30}" x2="{cx - 10}" y2="{cy + 14}" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
                f'<line x1="{cx + 20}" y1="{cy + 30}" x2="{cx + 10}" y2="{cy + 14}" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
            ]
        )
    elif kind == "speed":
        base.extend(
            [
                f'<path d="M {cx - 26} {cy + 20} A 38 38 0 0 1 {cx + 26} {cy + 20}" fill="none" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
                f'<line x1="{cx - 24}" y1="{cy + 10}" x2="{cx - 30}" y2="{cy + 4}" stroke="{PRIMARY}" stroke-width="3" stroke-linecap="round"/>',
                f'<line x1="{cx - 6}" y1="{cy - 2}" x2="{cx - 12}" y2="{cy - 10}" stroke="{PRIMARY}" stroke-width="3" stroke-linecap="round"/>',
                f'<line x1="{cx + 14}" y1="{cy - 2}" x2="{cx + 22}" y2="{cy - 10}" stroke="{PRIMARY}" stroke-width="3" stroke-linecap="round"/>',
                f'<circle cx="{cx}" cy="{cy + 10}" r="10" fill="{ACCENT}" fill-opacity="0.22" stroke="{PRIMARY}" stroke-width="3"/>',
                f'<line x1="{cx}" y1="{cy + 10}" x2="{cx + 20}" y2="{cy - 8}" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
            ]
        )
    elif kind == "chart":
        base.extend(
            [
                f'<rect x="{cx - 24}" y="{cy + 6}" width="10" height="20" rx="2" fill="{PRIMARY}"/>',
                f'<rect x="{cx - 8}" y="{cy - 2}" width="10" height="28" rx="2" fill="{PRIMARY}"/>',
                f'<rect x="{cx + 8}" y="{cy - 14}" width="10" height="40" rx="2" fill="{PRIMARY}"/>',
                f'<path d="M {cx - 24} {cy - 2} L {cx - 8} {cy + 2} L {cx + 12} {cy - 12} L {cx + 20} {cy - 24}" fill="none" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
                f'<line x1="{cx - 28}" y1="{cy + 34}" x2="{cx + 28}" y2="{cy + 34}" stroke="{PRIMARY}" stroke-width="4" stroke-linecap="round"/>',
            ]
        )
    return ''.join(base)


def summary_row(x: int, y: int, label: str, value: str) -> str:
    return ''.join(
        [
            text(x, y, f"{label}:", size=17, fill=TEXT_SUB, anchor="end"),
            text(x + 10, y, value, size=27, fill=PRIMARY, weight="700", anchor="start"),
        ]
    )


def summary_note_row(cx: int, y: int, content: str) -> str:
    return text(cx, y, content, size=16, fill=ACCENT, weight="700", anchor="middle")


def summary_panel(x: int, y: int, w: int, h: int, title: str, kind: str, rows: list[tuple[str, str]], note: str | None = None) -> str:
    cx = x + w // 2
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.4"/>',
        summary_icon(cx, y + 86, kind),
        text(cx, y + 178, title, size=22, fill=TEXT_MAIN, weight="700", anchor="middle"),
        f'<line x1="{x + 42}" y1="{y + 206}" x2="{x + w - 42}" y2="{y + 206}" stroke="{LINE}" stroke-width="1.5"/>',
    ]
    row_y = y + 250
    for label, value in rows:
        parts.append(summary_row(cx - 10, row_y, label, value))
        row_y += 42
    if note:
        parts.append(summary_note_row(cx, row_y - 2, note))
    return ''.join(parts)


def footer(page_num: str, source: str) -> str:
    return ''.join(
        [
            f'<rect x="0" y="640" width="1280" height="80" fill="{BG_LIGHT}"/>',
            f'<line x1="0" y1="640" x2="1280" y2="640" stroke="{LINE}" stroke-width="1"/>',
            text(48, 672, source, size=11, fill=TEXT_LIGHT),
            text(48, 696, "Design spec aligned | Native SVG for PPT export", size=11, fill=TEXT_LIGHT),
            f'<rect x="1148" y="652" width="84" height="30" rx="6" fill="{PRIMARY}"/>',
            text(1190, 672, page_num, size=14, fill="#FFFFFF", weight="700", anchor="middle"),
        ]
    )


def content_page(title: str, takeaway: str, body: str, page_num: str, chapter: str, replace_full_content_group: bool = False) -> str:
    page_indices = {
        "03": "一、",
        "04": "二、",
        "05": "三、",
        "06": "四、",
        "07": "五、",
        "08": "六、",
        "09": "七、",
        "10": "八、",
        "11": "九、",
    }
    notes = {
        "03": "Template: 03_content.svg | layout: background and growth path",
        "04": "Template: 03_content.svg | layout: objective cards",
        "05": "Template: 03_content.svg | layout: three summary panels",
        "06": "Template: 03_content.svg | layout: project case blocks",
        "07": "Template: 03_content.svg | layout: system build sequence",
        "08": "Template: 03_content.svg | layout: improvement comparison",
        "09": "Template: 03_content.svg | layout: contribution cards",
        "10": "Template: 03_content.svg | layout: improvement rows",
        "11": "Template: 03_content.svg | layout: future plan and support",
    }
    return render_content_template(
        title=title,
        takeaway=takeaway,
        body=body,
        page_num=page_num,
        section_name=chapter,
        page_index=page_indices[page_num],
        source="sources/personal_material.md | sources/content_requirement.md",
        note=notes[page_num],
        replace_full_content_group=replace_full_content_group,
    )


def render_cover() -> str:
    template = replace_tokens(
        load_template("01_cover.svg"),
        {
            "COVER_TITLE": escape("试用期转正述职报告"),
            "USERNAME": escape("方汉涛"),
            "DATE": escape("2026-04-04"),
            "FORM_CODE": escape("PROBATION-20260404"),
            "VERSION": escape("v2-template"),
        },
    )
    subtitle = (
        '<text font-family="Microsoft YaHei,Microsoft YaHei_MSFontService,sans-serif" '
        'font-weight="700" font-size="24" fill="#4F6475" transform="translate(709 618)">'
        '后端研发工程师 | 6年行业经验 | 入职6个月工作总结</text>'
    )
    return template.replace('</g></svg>', f'{subtitle}</g></svg>', 1)


def render_toc() -> str:
    return load_template("02_toc.svg")


def page_03() -> str:
    body = '''
    <g>
        <rect x="40" y="176" width="1200" height="430" rx="8" fill="#FFFFFF" stroke="#D8E7B4" stroke-width="1.5"/>
        <path fill="#F8FBF0" d="M72,214 C228,170 420,188 600,226 C760,259 923,252 1174,186 L1174,258 C1011,302 846,317 660,286 C455,252 241,250 72,292 Z"/>
        <path d="M96,486 L350,410 L620,446 L882,330 L1100,262" fill="none" stroke="#E7F0D8" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M96,486 L350,410 L620,446 L882,330 L1100,262" fill="none" stroke="#B9D99E" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M1100,262 L1148,222" fill="none" stroke="#B9D99E" stroke-width="8" stroke-linecap="round"/>
        <path d="M1142,214 L1178,214 L1156,247 Z" fill="#7F8C8D"/>

        <circle cx="350" cy="410" r="38" fill="#A8C66C"/>
        <circle cx="620" cy="446" r="36" fill="#88C100"/>
        <circle cx="882" cy="330" r="39" fill="#6FAE43"/>
        <circle cx="1100" cy="262" r="48" fill="#6CC04A" fill-opacity="0.18"/>
        <circle cx="1100" cy="262" r="40" fill="#6CC04A"/>

        <text x="350" y="419" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF">2016</text>
        <text x="620" y="455" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF">2019</text>
        <text x="882" y="339" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF">2025</text>
        <text x="1100" y="271" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="700" fill="#FFFFFF">当前</text>

        <text x="200" y="300" font-family="Microsoft YaHei, Arial, sans-serif" font-size="28" font-weight="700" fill="#7FA53A">教育背景</text>
        <text x="128" y="338" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">2016-2020 华南农业大学 软件工程</text>
        <text x="146" y="366" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">完成研发基础能力建立</text>

        <text x="520" y="574" font-family="Microsoft YaHei, Arial, sans-serif" font-size="28" font-weight="700" fill="#88C100">前司研发经历</text>
        <text x="420" y="610" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">2019-2025 深圳乐信控股有限公司</text>
        <text x="442" y="638" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">积累复杂业务交付与系统建设经验</text>

        <text x="760" y="194" font-family="Microsoft YaHei, Arial, sans-serif" font-size="28" font-weight="700" fill="#5F9E32">入职当前公司</text>
        <text x="724" y="228" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">2025.10 入职后快速切入会员、营销活动、运营平台</text>
        <text x="736" y="256" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#5D6D7E">完成从经验迁移到业务承担的过渡</text>

        <path fill="#F7FBF4" stroke="#B9D99E" stroke-width="1.4" d="M896,390 H1188 A12,12 0 0 1 1200,402 V548 A12,12 0 0 1 1188,560 H896 A12,12 0 0 1 884,548 V402 A12,12 0 0 1 896,390 Z"/>
        <rect x="884" y="390" width="316" height="10" rx="5" fill="#6CC04A"/>
        <text x="906" y="432" font-family="Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="700" fill="#4D7E2E">当前岗位定位</text>
        <text x="906" y="468" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#333F50">后端开发工程师</text>
        <text x="906" y="496" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#333F50">负责活动系统、会员权益、运营配置平台</text>
        <text x="906" y="524" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="400" fill="#333F50">兼顾交付效率、系统质量与复用沉淀</text>

        <path fill="#FFFFFF" stroke="#DDEACF" stroke-width="1" d="M906,574 H1040 A18,18 0 0 1 1058,592 V592 A18,18 0 0 1 1040,610 H906 A18,18 0 0 1 888,592 V592 A18,18 0 0 1 906,574 Z"/>
        <path fill="#FFFFFF" stroke="#DDEACF" stroke-width="1" d="M1070,574 H1168 A18,18 0 0 1 1186,592 V592 A18,18 0 0 1 1168,610 H1070 A18,18 0 0 1 1052,592 V592 A18,18 0 0 1 1070,574 Z"/>
        <path fill="#FFFFFF" stroke="#DDEACF" stroke-width="1" d="M906,620 H1022 A18,18 0 0 1 1040,638 V638 A18,18 0 0 1 1022,656 H906 A18,18 0 0 1 888,638 V638 A18,18 0 0 1 906,620 Z"/>
        <path fill="#FFFFFF" stroke="#DDEACF" stroke-width="1" d="M1052,620 H1168 A18,18 0 0 1 1186,638 V638 A18,18 0 0 1 1168,656 H1052 A18,18 0 0 1 1034,638 V638 A18,18 0 0 1 1052,620 Z"/>
        <text x="973" y="598" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" font-weight="700" fill="#4F5B66">复杂需求拆解</text>
        <text x="1119" y="598" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" font-weight="700" fill="#4F5B66">平台化设计</text>
        <text x="964" y="644" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" font-weight="700" fill="#4F5B66">项目统筹推进</text>
        <text x="1110" y="644" text-anchor="middle" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" font-weight="700" fill="#4F5B66">AI 协同研发</text>

        <rect x="56" y="556" width="768" height="34" rx="8" fill="#F6FBE8" stroke="#CFE1A8" stroke-width="1"/>
        <rect x="56" y="556" width="6" height="34" rx="3" fill="#88C100"/>
        <text x="76" y="579" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="700" fill="#4F5B66">已完成从既有研发经验到当前岗位担当的衔接，具备独立承接复杂事项的基础。</text>
    </g>'''
    return content_page(
        "个人背景与岗位定位",
        "从教育积累到 5 年研发实践，再到入职后快速切入核心业务，已完成从经验迁移到岗位担当的衔接。",
        body,
        "03",
        "个人背景与岗位认知",
        replace_full_content_group=True,
    )


def page_04() -> str:
    body = ''.join(
        [
            info_card(58, 210, 348, 220, "ROLE", "试用期举证", ["活动项目四期按期交付", "规则引擎从0到1独立落地", "CRM与转盘优化体现提效"], accent=PRIMARY),
            info_card(466, 210, 348, 220, "TARGET", "岗位理解", ["关键项目里要扛住结果", "复杂问题上要给出方案", "一次性交付要沉淀为复用能力"], accent=ACCENT),
            info_card(874, 210, 348, 220, "STANDARD", "对自己的要求", ["覆盖项目负责、独立建设、效率优化", "让团队能放心交付复杂事项"], accent=POSITIVE),
            f'<rect x="58" y="470" width="1164" height="94" rx="16" fill="{SECONDARY}"/>',
            multiline_text(86, 520, ["试用期要证明的，不只是做了多少功能，而是能否持续承担复杂事项。"], size=26, fill=PRIMARY, weight="700", line_gap=32),
        ]
    )
    return content_page(
        "岗位认知与试用期目标",
        "用试用期实际交付结果，反证我对岗位要求的理解。",
        body,
        "04",
        "01 BACKGROUND",
    )


def page_05() -> str:
    body_parts = [
        '\t<g>',
        '\t\t<rect x="40" y="176" width="1200" height="430" rx="8" fill="#FFFFFF"/>',
        summary_panel(58, 188, 356, 372, "核心业绩指标", "target", [("重点事项覆盖", "10项"), ("已完成交付", "8项"), ("按期交付率", "100%")]),
        summary_panel(432, 188, 356, 372, "效率与能力提升", "speed", [("CRM查询", "2s → 1s以下"), ("配置时间", "1天 → 2小时")], note="体验显著改善，复用性提升"),
        summary_panel(806, 188, 356, 372, "业务成果与价值", "chart", [("积分提醒覆盖", "40w+"), ("拉新活动转化", "1992人"), ("活动参与人数", "16045人")]),
        '\t</g>',
    ]
    return content_page(
        "整体产出与量化结果：全面达成与价值交付",
        "各项成果全面达成，在交付效率、系统性能和业务价值上均有显著贡献。",
        ''.join(body_parts),
        "05",
        "02 RESULTS",
        replace_full_content_group=True,
    )


def page_06() -> str:
    body = ''.join(
        [
            metric_card(58, 186, 214, 108, "项目周期", "2025.11 - 2025.12", "持续两个月、四期推进"),
            metric_card(294, 186, 214, 108, "一期上线", "19 个工作日", "高压周期下按时交付"),
            metric_card(530, 186, 214, 108, "项目投入", "4 后端 + 3 前端", "多角色协同复杂"),
            metric_card(766, 186, 456, 108, "个人角色", "项目负责人 + 核心研发", "同时承担节奏统筹和关键研发"),
            info_card(58, 326, 270, 204, "SITUATION", "高压项目背景", ["需求范围大、时间紧、业务目标强", "活动需兼顾拉新、活跃和转化"], accent=PRIMARY),
            info_card(348, 326, 270, 204, "TASK", "承担什么责任", ["拆解发布节奏", "协调前后端与业务方", "承担关键模块研发和风险兜底"], accent=ACCENT),
            info_card(638, 326, 270, 204, "ACTION", "关键动作", ["识别核心链路和里程碑", "分期推进联调、提测、上线", "发现问题后快速协调修复"], accent=POSITIVE),
            info_card(928, 326, 294, 204, "RESULT", "最终结果", ["12.23 完成第四期发布", "活动拉新 1992 人、参与 16045 人", "完成线上问题快速修复与协同兜底"], accent=WARNING),
        ]
    )
    return content_page(
        "关键案例一｜圣诞与新年活动高压交付",
        "在时间紧、范围大、协同复杂的条件下，完成四期活动稳定落地。",
        body,
        "06",
        "02 RESULTS",
    )


def page_07() -> str:
    body = ''.join(
        [
            f'<rect x="58" y="196" width="1164" height="112" rx="16" fill="{SECONDARY}"/>',
            multiline_text(88, 238, ["从原型、文档到系统实现形成完整闭环，证明独立建设复杂系统的能力。"], size=26, fill=PRIMARY, weight="700", line_gap=30),
            text(88, 282, "系统支持调用集、规则链、规则测试执行和多环境管理。", size=18, fill=TEXT_SUB),
            info_card(58, 344, 250, 186, "01", "原型设计", ["自绘原型交互", "在方案阶段提前定义边界与流程"], accent=PRIMARY),
            info_card(332, 344, 250, 186, "02", "需求文档", ["自编管理台需求文档", "降低后续协作理解偏差"], accent=ACCENT),
            info_card(606, 344, 250, 186, "03", "系统实现", ["独立实现规则引擎系统", "完成管理台和执行能力建设"], accent=POSITIVE),
            info_card(880, 344, 342, 186, "04", "价值结论", ["从需求承接升级为方案定义与独立交付", "体现更强的抽象设计和 ownership 能力"], accent=WARNING),
        ]
    )
    return content_page(
        "关键案例二｜规则引擎从0到1独立建设",
        "从原型、文档到系统实现形成完整闭环，证明独立建设复杂系统的能力。",
        body,
        "07",
        "02 RESULTS",
    )


def page_08() -> str:
    body = ''.join(
        [
            info_card(58, 204, 356, 310, "CASE A", "CRM 查询优化", ["问题：后台查询接口响应慢", "动作：定位瓶颈并重构查询链路", "结果：2s → 1s以下", "价值：直接提升运营侧使用效率"], accent=PRIMARY),
            info_card(462, 204, 356, 310, "CASE B", "签到重构", ["问题：活动需求重复开发", "动作：抽象为标准配置化能力", "结果：后端无需每次重复开发", "价值：提升需求响应效率与稳定性"], accent=ACCENT),
            info_card(866, 204, 336, 310, "CASE C", "转盘配置化", ["问题：33 个子类散落在实现中", "动作：收敛为配置组合", "结果：新增活动 1 天 → 2h", "价值：持续降低重复研发成本"], accent=POSITIVE),
            f'<rect x="58" y="540" width="1144" height="44" rx="12" fill="{PRIMARY}" fill-opacity="0.06"/>',
            text(80, 568, "通过性能优化、架构重构和配置化设计，把一次性交付持续升级为可复用能力。", size=20, fill=PRIMARY, weight="700"),
        ]
    )
    return content_page(
        "关键案例三｜优化与平台化建设",
        "不只完成需求，更持续把一次性交付升级成可复用能力。",
        body,
        "08",
        "02 RESULTS",
    )


def page_09() -> str:
    body = ''.join(
        [
            info_card(58, 210, 270, 242, "沉淀 01", "新人指引", ["编写《后端研发新人指引》", "帮助新同学更快理解环境、流程和协作方式"], accent=PRIMARY),
            info_card(348, 210, 270, 242, "沉淀 02", "工程 SOP", ["梳理新增工程应用 SOP", "梳理上线应用 SOP", "降低重复沟通成本"], accent=ACCENT),
            info_card(638, 210, 270, 242, "沉淀 03", "AI 协同研发", ["在需求分析、文档整理、代码辅助中实践 AI 方法", "提升信息组织和研发效率"], accent=POSITIVE),
            info_card(928, 210, 294, 242, "沉淀 04", "团队价值", ["把个人经验沉淀成团队可复用资产", "降低 onboarding 和交接成本"], accent=WARNING),
            f'<rect x="58" y="486" width="1164" height="82" rx="16" fill="{SECONDARY}"/>',
            multiline_text(86, 530, ["在项目交付之外，主动补位团队机制与知识沉淀，让经验可以复制、方法可以复用。"], size=25, fill=PRIMARY, weight="700", line_gap=30),
        ]
    )
    return content_page(
        "个人贡献与方法沉淀",
        "在项目交付之外，主动补位团队机制与知识沉淀。",
        body,
        "09",
        "03 EXTRA VALUE",
    )


def page_10() -> str:
    rows = [
        ("结果量化不足", "提前定义效果指标", "在项目开始阶段同步效果口径，避免复盘时只有过程没有结果。"),
        ("业务纵深不足", "系统梳理会员与营销链路", "不只完成模块交付，还进一步补足业务全链路理解。"),
        ("AI 规范沉淀不足", "建设项目级 context 和协作规范", "把个人实践沉淀成团队可复用的方法论和协作约束。"),
    ]
    parts: list[str] = []
    y = 206
    for title_label, action, detail in rows:
        parts.extend(
            [
                f'<rect x="58" y="{y}" width="1164" height="102" rx="14" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.2"/>',
                f'<rect x="58" y="{y}" width="14" height="102" rx="7" fill="{PRIMARY}"/>',
                text(94, y + 36, title_label, size=21, fill=TEXT_MAIN, weight="700"),
                text(396, y + 36, action, size=20, fill=PRIMARY, weight="700"),
                multiline_text(694, y + 36, [detail], size=17, fill=TEXT_SUB, line_gap=24),
            ]
        )
        y += 122
    return content_page(
        "不足与提升计划",
        "已识别在量化、业务纵深和团队级规范方面的提升空间。",
        ''.join(parts),
        "10",
        "03 EXTRA VALUE",
    )


def page_11() -> str:
    body = ''.join(
        [
            info_card(58, 208, 548, 278, "PLAN", "未来 6 个月计划", ["4月：深化 AI 工具使用，继续缩短交付周期", "5月：打造项目级 context，沉淀团队经验", "6月：推进营销活动平台建设，争取 Q2 完成核心能力"], accent=PRIMARY),
            info_card(634, 208, 568, 278, "SUPPORT", "建议与求助", ["为平台化事项预留稳定排期", "提供跨团队协同与数据复盘支持", "帮助关键能力建设获得更持续的资源保障"], accent=ACCENT),
            f'<rect x="58" y="516" width="1144" height="54" rx="14" fill="{PRIMARY}" fill-opacity="0.06"/>',
            text(84, 549, "已具备持续承担更大职责的基础，申请按期转正，并继续围绕 AI 提效、平台建设和经验沉淀投入。", size=19, fill=PRIMARY, weight="700"),
        ]
    )
    return content_page(
        "未来计划、建议与求助",
        "未来继续围绕 AI 提效、平台建设和团队经验沉淀三个方向持续投入。",
        body,
        "11",
        "04 NEXT STEP",
    )


def render_ending() -> str:
    return replace_tokens(
        load_template("04_ending.svg"),
        {
            "THANKS_TITLE": escape("感谢聆听"),
            "THANKS_SUBTITLE": escape("欢迎各位领导和同事指正"),
        },
    )


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