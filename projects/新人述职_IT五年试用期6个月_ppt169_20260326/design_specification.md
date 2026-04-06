# Design Specification & Content Outline

## I. Project Information

| Field | Value |
|---|---|
| Project Name | 方汉涛试用期转正述职（工作6年，试用期6个月） |
| Canvas Format | PPT 16:9 |
| Canvas Size | 1280  720 |
| ViewBox | 0 0 1280 720 |
| Target Page Count | 12 pages |
| Style Objective | B) General Consulting |
| Audience | 直属领导、部门负责人、HR |
| Scenario | 试用期转正述职 / 阶段性汇报 |
| Date | 2026-04-04 |

## II. Canvas Specification

| Item | Spec |
|---|---|
| Safe Area | x:60-1220, y:60-680 |
| Header | y:0-80 |
| Content Area | y:100-620 |
| Footer | y:640-720 |
| Grid | 40px baseline |

## III. Visual Theme

- Theme: McKinsey light consulting style (white background + blue accents)
- Tone: Structured, concise, data-first, conclusion-oriented

### Color Palette

| Role | HEX | Usage |
|---|---|---|
| Primary | #005587 | Title bars, key headings |
| Secondary | #EAF3F8 | Data cards, light panels |
| Accent | #00A3E0 | Highlighted points |
| Positive | #2E7D32 | Positive KPI / completion |
| Warning | #F5A623 | Risks / pending items |
| Negative | #C62828 | Issues / blocker tags |
| Text Main | #2C3E50 | Main text |
| Text Sub | #5D6D7E | Secondary text |

## IV. Typography System

| Role | Font |
|---|---|
| Title | Microsoft YaHei, Arial |
| Body | Microsoft YaHei, Calibri |
| Emphasis | SimHei, Arial Bold |

| Level | Size |
|---|---|
| Cover Title | 56px |
| Page Title | 30px |
| Section Title | 22px |
| Body | 18px |
| Annotation | 14px |
| Footer/Source | 12px |

## V. Layout Principles

- Follow template framework: cover/toc/profile/objective/content/summary/ending
- Content pages adopt: profile timeline, KPI cards, case-study pages, comparison cards, roadmap
- Keep one core takeaway per page and present evidence directly under the conclusion
- Use consistent footer source and page numbering
- Prefer diagrams, cards, timelines, and structural visuals over prose blocks
- Prefer 3-5 evidence points per page and keep each point within 2 lines

## VI. Icon Usage Specification

- Icon Source: Built-in icon library (`templates/icons/icons_index.json`)
- Usage Mode: `<use data-icon="icon-name" .../>`, embedded by `finalize_svg.py`

### Approved Icon Inventory

- chart-bar
- arrow-trend-up
- circle-checkmark
- users
- target
- clock
- lightbulb
- server

## VII. Chart Reference List

| Chart Type | Reference | Used In | Purpose |
|---|---|---|---|
| kpi_cards | templates/charts/kpi_cards.svg | 05_6m_kpi | 试用期整体产出与量化结果 |
| timeline_horizontal | templates/charts/timeline_horizontal.svg | 06_project_cases | 圣诞与新年活动四期项目节奏 |
| grouped_bar_chart | templates/charts/grouped_bar_chart.svg | 08_improvement_actions | 性能优化与配置化改造前后对比 |
| fishbone_chart | templates/charts/fishbone_chart.svg | 10_risk_support | 当前不足与改进方向拆解 |
| timeline_horizontal | templates/charts/timeline_horizontal.svg | 11_value_summary | 未来6个月工作里程碑 |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Layout Suggestion | Purpose | Type | Status | Generation Description |
|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | This deck is data-first, no image needed | N/A | Not required | N/A |

## IX. Content Outline

### 01_cover
- Title: 试用期转正述职报告
- Subtitle: 后端研发工程师 | 6年行业经验 | 入职6个月工作总结
- Core message: 在试用期内完成从快速融入到独立承担、从需求交付到系统沉淀的阶段性转变
- Layout: 大标题封面 + 右下角信息块
- Key modules: 主标题、副标题、核心结论条、方汉涛/岗位/入职时间/汇报日期

### 02_toc
- 目录：个人背景与岗位认知、整体产出与关键案例、个人沉淀与不足、未来计划与转正申请
- Layout: 四段式目录导航
- Key modules: 页标题、结论条、4个目录卡片、章节编号

### 03_chapter
- 个人基本情况：工作背景、岗位定位、当前职责与角色承担
- Layout: 横向上升式时间轴 + 节点说明块
- Key modules: 4个时间节点、经历与角色变化说明、当前岗位说明、业务方向、能力标签

### 04_role_transition
- 岗位认知与试用期目标：独立承接需求、承担复杂项目、沉淀可复用机制
- Layout: 三列目标卡 + 底部总结条
- Key modules: 岗位理解、3个试用期目标卡片、阶段结论

### 05_6m_kpi
- 6个月整体产出：覆盖10项重点事项，其中8项完成交付，2项形成方案沉淀或交接，并给出核心量化成果
- Layout: KPI卡片 + 底部证据说明
- Key modules: 4张KPI卡片、核心数字、业务结果摘要、结果说明条

### 06_project_cases
- 关键案例一：圣诞与新年活动高压交付，突出项目统筹、核心研发、业务结果与风险兜底能力
- Layout: 左时间轴 + 右项目说明
- Key modules: 四期项目时间轴、项目背景、个人职责、项目难点、项目结果、拉新/参与数据

### 07_problem_analysis
- 关键案例二：规则引擎从0到1独立建设，突出方案设计、原型文档和系统实现闭环
- Layout: 闭环流程图 + 右侧价值总结
- Key modules: 原型设计、需求文档、系统设计、后端实现、测试执行、价值总结

### 08_improvement_actions
- 关键案例三：性能优化、签到重构、转盘配置化，突出平台化建设、效率提升与复用价值
- Layout: 三栏案例对比页
- Key modules: CRM查询优化、签到重构、转盘配置化、每栏前后对比结果、关键数字

### 09_next_6m_plan
- 个人贡献与方法沉淀：新人指引、上线SOP、AI协同研发实践等团队资产
- Layout: 左侧成果列表 + 右侧价值映射
- Key modules: 做了什么、解决了什么问题、成果到价值的映射关系、团队收益说明

### 10_risk_support
- 不足与提升计划：结果量化、业务纵深、团队级AI规范沉淀三方面改进方向
- Layout: 三行问题改进表
- Key modules: 不足项、影响说明、改进行动

### 11_value_summary
- 未来计划、建议与求助：AI研发提效、项目级context、营销活动平台Q2建设与组织支持事项
- Layout: 上时间轴 + 下支持事项双栏
- Key modules: 未来6个月里程碑、建议事项、求助事项、阶段目标、转正申请结论

### 12_ending
- 总结、转正申请与现场答疑
- Layout: 总结页 + 问答引导
- Key modules: 3条总结、感谢语、Q&A提示

## X. Speaker Notes Plan

| Field | Value |
|---|---|
| Total Duration | 15-18 minutes |
| Notes Style | Formal + concise + conclusion-first |
| Purpose | Report + persuade |
| Transition Rule | From page 2 onward, each page starts with [Transition] |
