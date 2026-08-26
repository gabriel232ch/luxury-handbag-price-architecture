from __future__ import annotations

import csv
import html
import math
import os
from collections import defaultdict


ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "final_report_assets")
os.makedirs(OUT, exist_ok=True)


COLORS = {
    "CHANEL": "#171717",
    "Hermès": "#8C4A24",
    "Louis Vuitton": "#B07A3D",
    "Dior": "#7D2947",
}
BRANDS = ["CHANEL", "Hermès", "Louis Vuitton", "Dior"]
BRAND_LABELS = {"CHANEL": "Chanel", "Hermès": "Hermès", "Louis Vuitton": "Louis Vuitton", "Dior": "Dior"}
FONT = "'Noto Sans CJK SC','PingFang SC','Heiti SC','Arial',sans-serif"


def read_csv(rel):
    with open(os.path.join(ROOT, rel), newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def esc(value):
    return html.escape(str(value), quote=True)


def fmt_num(value, currency=None):
    if value is None or value == "":
        return "—"
    n = float(value)
    if abs(n - round(n)) < 1e-8:
        s = f"{int(round(n)):,}"
    else:
        s = f"{n:,.1f}"
    if currency:
        return ("€" if currency == "EUR" else "$") + s
    return s


def svg_start(width, height, title, subtitle=""):
    return [
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">''',
        f'''<rect width="{width}" height="{height}" fill="#FCFBF8"/>''',
        f'''<style>
          .title {{ font-family:{FONT}; font-size:28px; font-weight:700; fill:#1F2933; }}
          .subtitle {{ font-family:{FONT}; font-size:15px; fill:#5B6570; }}
          .section {{ font-family:{FONT}; font-size:18px; font-weight:700; fill:#1F2933; }}
          .label {{ font-family:{FONT}; font-size:14px; fill:#39424E; }}
          .small {{ font-family:{FONT}; font-size:12px; fill:#65717C; }}
          .note {{ font-family:{FONT}; font-size:12px; fill:#66727C; }}
          .value {{ font-family:{FONT}; font-size:13px; font-weight:700; fill:#25313B; }}
          .grid {{ stroke:#D8D5CF; stroke-width:1; }}
          .axis {{ stroke:#8D959C; stroke-width:1.2; }}
        </style>''',
        f'''<text x="56" y="52" class="title">{esc(title)}</text>''',
    ] + ([f'''<text x="56" y="79" class="subtitle">{esc(subtitle)}</text>'''] if subtitle else [])


def svg_end(lines):
    lines.append("</svg>")
    return "\n".join(lines)


def save(name, lines):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg_end(lines))


def xscale(value, lo, hi, left, right):
    return left + (float(value) - lo) / (hi - lo) * (right - left)


def axis_ticks(lines, lo, hi, left, right, y, currency, step):
    tick = math.ceil(lo / step) * step
    while tick <= hi + 0.001:
        x = xscale(tick, lo, hi, left, right)
        lines.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y+260}" class="grid"/>')
        lines.append(f'<text x="{x:.1f}" y="{y+284}" text-anchor="middle" class="small">{fmt_num(tick, currency)}</text>')
        tick += step


def chart_current_architecture():
    rows = read_csv("competitive_pricing_calculations/brand_price_summary.csv")
    data = {(r["brand"], r["market"]): r for r in rows}
    width, height = 1600, 900
    lines = svg_start(width, height, "四品牌当前价格架构", "法国与美国分面；横线为可见数值价格范围，粗线为中间 50% 区间，圆点为中位数。")
    panels = [("FR", "法国｜EUR", "EUR", 0, 14000), ("US", "美国｜USD", "USD", 0, 15000)]
    lefts = [90, 850]
    for (market, panel_title, currency, lo, hi), left in zip(panels, lefts):
        right = left + 640
        top = 150
        lines.append(f'<text x="{left}" y="{top}" class="section">{panel_title}</text>')
        axis_ticks(lines, lo, hi, left + 150, right - 20, top + 32, currency, 2000)
        for idx, brand in enumerate(BRANDS):
            y = top + 90 + idx * 118
            r = data[(brand, market)]
            lines.append(f'<text x="{left+140}" y="{y+5}" text-anchor="end" class="label">{esc(BRAND_LABELS[brand])}</text>')
            x0 = xscale(r["minimum"], lo, hi, left + 160, right - 20)
            x1 = xscale(r["maximum"], lo, hi, left + 160, right - 20)
            q1 = xscale(r["lower_quartile_p25"], lo, hi, left + 160, right - 20)
            q3 = xscale(r["upper_quartile_p75"], lo, hi, left + 160, right - 20)
            med = xscale(r["median_p50"], lo, hi, left + 160, right - 20)
            color = COLORS[brand]
            lines.append(f'<line x1="{x0:.1f}" y1="{y}" x2="{x1:.1f}" y2="{y}" stroke="{color}" stroke-width="5" stroke-linecap="round" opacity="0.55"/>')
            lines.append(f'<line x1="{q1:.1f}" y1="{y}" x2="{q3:.1f}" y2="{y}" stroke="{color}" stroke-width="18" stroke-linecap="round"/>')
            lines.append(f'<circle cx="{med:.1f}" cy="{y}" r="8" fill="#FCFBF8" stroke="{color}" stroke-width="4"/>')
            lines.append(f'<text x="{right-10}" y="{y+5}" text-anchor="end" class="value">{fmt_num(r["median_p50"], currency)}</text>')
            lines.append(f'<text x="{x0:.1f}" y="{y-20}" text-anchor="middle" class="small">{fmt_num(r["minimum"], currency)}</text>')
            lines.append(f'<text x="{x1:.1f}" y="{y-20}" text-anchor="middle" class="small">{fmt_num(r["maximum"], currency)}</text>')
        lines.append(f'<text x="{left+160}" y="{top+565}" class="note">范围 = min–max；粗线 = P25–P75；点 = 中位数</text>')
    lines.append('<line x1="56" y1="760" x2="1544" y2="760" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="790" class="note">主读法：Chanel 的可见起点更高；Louis Vuitton / Dior 密集于较低层；Hermès 的观察范围更宽。各市场使用本地货币，不合并比较。</text>')
    lines.append('<text x="56" y="815" class="note">样本注：2026-08-15 官方页面采样；161 条接受观察、147 条数值价格；非加权快照，非全量产品普查。</text>')
    save("01_four_brand_current_architecture.svg", lines)


def chart_band_battleground():
    rows = read_csv("competitive_pricing_calculations/price_band_summary.csv")
    bands = ["Access / lower", "Core", "Premium core", "High", "Exceptional / icon"]
    band_labels = {"Access / lower": "Access / lower", "Core": "Core", "Premium core": "Premium core", "High": "High", "Exceptional / icon": "Exceptional / icon"}
    width, height = 1600, 900
    lines = svg_start(width, height, "价格带战场：竞争集合随层级变化", "每个单元格为“数值观察数（占该品牌本地数值样本）”；0 表示本次采样没有捕获数值观察，不表示品牌全球没有该价格带产品。")
    panels = [("FR", "法国｜EUR", 80), ("US", "美国｜USD", 850)]
    for market, title, left in panels:
        top = 150
        cell_w, cell_h = 145, 70
        label_w = 160
        lines.append(f'<text x="{left}" y="{top}" class="section">{title}</text>')
        for j, brand in enumerate(BRANDS):
            x = left + label_w + j * cell_w + cell_w / 2
            lines.append(f'<text x="{x}" y="{top+38}" text-anchor="middle" class="label">{esc(BRAND_LABELS[brand])}</text>')
        lookup = {(r["brand"], r["band"]): r for r in rows if r["market"] == market}
        max_count = max(int(r["numeric_observations"]) for r in lookup.values())
        for i, band in enumerate(bands):
            y = top + 60 + i * cell_h
            lines.append(f'<text x="{left+label_w-14}" y="{y+42}" text-anchor="end" class="label">{esc(band_labels[band])}</text>')
            for j, brand in enumerate(BRANDS):
                r = lookup[(brand, band)]
                x = left + label_w + j * cell_w
                count = int(r["numeric_observations"])
                intensity = 0.07 + 0.72 * (count / max_count if max_count else 0)
                color = COLORS[brand]
                lines.append(f'<rect x="{x}" y="{y}" width="{cell_w-4}" height="{cell_h-4}" rx="4" fill="{color}" opacity="{intensity:.2f}" stroke="#E5E2DC"/>')
                fg = "#FFFFFF" if intensity > 0.45 else "#26313B"
                lines.append(f'<text x="{x+cell_w/2-2}" y="{y+29}" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="{fg}">{count}</text>')
                lines.append(f'<text x="{x+cell_w/2-2}" y="{y+50}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{fg}">{esc(r["share_of_brand_numeric"])}</text>')
        lines.append(f'<text x="{left+label_w}" y="{top+60+5*cell_h+32}" class="note">观察到的价格带为分析分组，不是消费者可负担性分组。</text>')
    lines.append('<line x1="56" y1="760" x2="1544" y2="760" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="790" class="note">主读法：LV 在 lower/access 最密集；Dior 在法国 core 最集中；Chanel 在 premium-core 与 exceptional/icon 层更突出；Hermès 跨越多个层级并拥有较宽上尾。</text>')
    lines.append('<text x="56" y="815" class="note">来源：competitive_pricing_calculations/price_band_summary.csv；分带阈值按市场分别设定，EUR 与 USD 不在同一数值轴上。</text>')
    save("02_price_band_battleground.svg", lines)


def chart_chanel_ladder():
    family_rows = read_csv("competitive_pricing_calculations/family_price_summary.csv")
    width, height = 1600, 900
    lines = svg_start(width, height, "Chanel 当前价格梯：lower/core → Classic/icon → 询价上端", "仅展示本次官方页面采样中可见的 Chanel 家族区间；灰色询价标记不映射到数值轴。")
    panels = [("FR", "法国｜EUR", "EUR", 0, 13500, 90), ("US", "美国｜USD", "USD", 0, 15000, 850)]
    groups = [
        ("Mini Classic", "lower", "Core"),
        ("Shopping Bag", "lower", "Premium core"),
        ("Bowling Bag", "lower", "Premium core"),
        ("Classic 11.12", "icon", "Exceptional / icon"),
        ("Small Classic", "icon", "Exceptional / icon"),
    ]
    for market, title, currency, lo, hi, left in panels:
        top = 150
        right = left + 630
        plot_left, plot_right = left + 200, right - 20
        lines.append(f'<text x="{left}" y="{top}" class="section">{title}</text>')
        axis_ticks(lines, lo, hi, plot_left, plot_right, top + 32, currency, 2500)
        lookup = {(r["product_family"], r["market"]): r for r in family_rows if r["brand"] == "CHANEL" and r["market"] == market}
        for idx, (family, group, band) in enumerate(groups):
            y = top + 90 + idx * 68
            r = lookup[(family, market)]
            color = "#B07A3D" if group == "lower" else "#171717"
            x0 = xscale(r["minimum"], lo, hi, plot_left, plot_right)
            x1 = xscale(r["maximum"], lo, hi, plot_left, plot_right)
            lines.append(f'<text x="{plot_left-14}" y="{y+5}" text-anchor="end" class="label">{esc(family)}</text>')
            lines.append(f'<line x1="{x0:.1f}" y1="{y}" x2="{x1:.1f}" y2="{y}" stroke="{color}" stroke-width="16" stroke-linecap="round"/>')
            lines.append(f'<text x="{x1+10:.1f}" y="{y+5}" class="value">{fmt_num(r["minimum"], currency)}–{fmt_num(r["maximum"], currency)}</text>')
        gap_l = xscale(6700 if market == "FR" else 7400, lo, hi, plot_left, plot_right)
        gap_r = xscale(10000 if market == "FR" else 11000, lo, hi, plot_left, plot_right)
        gap_y = top + 90 + 3 * 68
        lines.append(f'<line x1="{gap_l:.1f}" y1="{gap_y-30}" x2="{gap_r:.1f}" y2="{gap_y-30}" stroke="#9B6B40" stroke-width="2" stroke-dasharray="5 5"/>')
        lines.append(f'<line x1="{gap_l:.1f}" y1="{gap_y-38}" x2="{gap_l:.1f}" y2="{gap_y-22}" stroke="#9B6B40" stroke-width="2"/>')
        lines.append(f'<line x1="{gap_r:.1f}" y1="{gap_y-38}" x2="{gap_r:.1f}" y2="{gap_y-22}" stroke="#9B6B40" stroke-width="2"/>')
        gap = "€3,300" if market == "FR" else "$3,600"
        lines.append(f'<text x="{(gap_l+gap_r)/2:.1f}" y="{gap_y-42}" text-anchor="middle" class="small">可见区间价差约 {gap}</text>')
        por_y = top + 90 + 5 * 68
        lines.append(f'<text x="{plot_left-14}" y="{por_y+5}" text-anchor="end" class="label">Classic 11.12 询价</text>')
        lines.append(f'<rect x="{plot_left}" y="{por_y-12}" width="280" height="24" rx="12" fill="#D4D1CA" opacity="0.8"/>')
        lines.append(f'<text x="{plot_left+140}" y="{por_y+5}" text-anchor="middle" class="small">3 条记录｜不显示数值</text>')
        lines.append(f'<text x="{left}" y="{top+565}" class="note">lower/core = Mini、Shopping、Bowling；Classic/icon = Classic 11.12、Small Classic</text>')
    lines.append('<line x1="56" y1="780" x2="1544" y2="780" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="810" class="note">主读法：Chanel 的可见价格不是一条均匀上升的连续梯，而是 lower/core 集群与 Classic/icon 集群之间存在明显跳升，上端还部分转为询价。</text>')
    lines.append('<text x="56" y="835" class="note">边界：本图描述捕获到的数值样本；遗漏的中间 SKU 或询价产品可能改变完整在售组合的梯形。</text>')
    save("03_chanel_current_ladder.svg", lines)


def chart_historical_icon_access():
    rows = read_csv("historical_pricing_calculations/icon_core_evolution.csv")
    width, height = 1600, 900
    lines = svg_start(width, height, "Chanel 法国选定产品线：图标与 Mini/access 价格演化", "2022–2026 共同观察年份；Classic 11.12 / Small Classic 对比两条 Mini Classic 线，非 Chanel 全部手袋组合。")
    left, right, top, bottom = 140, 1120, 160, 610
    maxv = 11500
    for tick in range(0, 12000, 2000):
        y = bottom - (tick / maxv) * (bottom - top)
        lines.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-14}" y="{y+5:.1f}" text-anchor="end" class="small">€{tick:,}</text>')
    years = [r["observed_year"] for r in rows]
    xs = {year: left + i * (right-left)/(len(years)-1) for i, year in enumerate(years)}
    lines.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>')
    for year, x in xs.items():
        lines.append(f'<text x="{x:.1f}" y="{bottom+34}" text-anchor="middle" class="label">{year}</text>')
    series = [("icon_median", "图标中位数", "#171717"), ("access_core_median", "Mini/access 中位数", "#B07A3D")]
    for key, label, color in series:
        pts = []
        for r in rows:
            x = xs[r["observed_year"]]
            y = bottom - (float(r[key]) / maxv) * (bottom-top)
            pts.append((x, y, r[key]))
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)
        lines.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="4"/>')
        for x, y, value in pts:
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#FCFBF8" stroke="{color}" stroke-width="4"/>')
            lines.append(f'<text x="{x:.1f}" y="{y-14:.1f}" text-anchor="middle" class="small">€{float(value):,.0f}</text>')
        lastx, lasty, _ = pts[-1]
        lines.append(f'<text x="{lastx+18:.1f}" y="{lasty+5:.1f}" class="value" fill="{color}">{label}</text>')
    lines.append('<rect x="1190" y="180" width="330" height="250" rx="10" fill="#F1EEE8" stroke="#D8D5CF"/>')
    lines.append('<text x="1220" y="220" class="section">结论</text>')
    notes = [
        "图标中位数：+18.1%",
        "Mini/access 中位数：+16.5%",
        "比例：2.05× → 2.08×",
        "绝对价差：€4,470 → €5,350",
        "两组价格都上移；图标仅适度领先。",
    ]
    for i, note in enumerate(notes):
        lines.append(f'<text x="1220" y="{257+i*32}" class="label">{esc(note)}</text>')
    lines.append('<text x="140" y="700" class="note">解释：这支持“广泛重定价 + 持续的高图标锚点”，而不是“只有图标产品大幅涨价”。</text>')
    lines.append('<text x="140" y="726" class="note">方法注：使用 common observed years，不插值；历史非当前观察主要来自已登记的专业二手历史价格表，2026 端点来自官方当前页面。</text>')
    lines.append('<text x="140" y="752" class="note">来源：historical_pricing_calculations/icon_core_evolution.csv；选定 Chanel France lineages：CH-C01、CH-C02、CH-C03、CH-C04。</text>')
    save("04_chanel_historical_icon_access.svg", lines)


def chart_archetype_matrix():
    width, height = 1800, 1080
    lines = svg_start(width, height, "四品牌价格架构原型与证据强度", "分析性标签，不是品牌官方战略声明；历史结论按同款连续与 successor 路径区分。")
    x0, y0 = 50, 135
    widths = [150, 280, 330, 300, 350, 290]
    headers = ["品牌", "观察到的进入门槛", "价格梯结构", "上端机制", "历史重定价证据", "主要限制"]
    rows = [
        ["Chanel", "高；FR €4,850 / US $5,400 起", "lower/core 集群 → Classic/icon 明显跳升；中间数值观察较薄", "Classic 11.12 / Small Classic 高锚点；部分 Classic 询价", "France 4 条 SAME_MODEL_CONTINUOUS；图标 +18.1%，access +16.5%；绝对价差扩大", "当前样本非全量；历史主要为法国选定 lineages；无 US 历史对照"],
        ["Louis Vuitton", "低；FR €1,800 / US $1,950 起", "较宽的 lower/core 可进入梯；观察重心偏低", "当前样本未见数值 exceptional 层", "四条 lineages 均有正向事件；Speedy 20 / Neverfull 同款路径支持 broad repricing", "Speedy / Alma successor 只能方向性解释；FR 与 US 当前组合不同"],
        ["Dior", "中；FR €3,000 / US $3,600 起", "压缩的 core / mid-premium 梯；法国数值观察集中在 core", "当前样本没有数值 exceptional 层", "3 条 lineages 全为 MODEL_SUCCESSOR；排除当前锚点转移后事件更温和", "US 仍有 7 条未解析；材质 / 版本变化与涨价难分"],
        ["Hermès", "有较低进入点；FR €2,170 / US $3,075 起", "宽广、多系列，中间层与上尾变化较大", "上端尾部更分散；US 进入 exceptional 观察", "仅 Geta / Jypsière 两条产品线；Geta France 存在来源冲突", "历史不足以讲组合层面重定价；无对称 icon 分类"],
    ]
    x_positions = [x0]
    for w in widths[:-1]:
        x_positions.append(x_positions[-1] + w)
    row_h = 178
    header_h = 58
    for j, (x, w, h) in enumerate(zip(x_positions, widths, headers)):
        lines.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{header_h}" fill="#26313B"/>')
        lines.append(f'<text x="{x+w/2}" y="{y0+36}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#FFFFFF">{esc(h)}</text>')
    for i, row in enumerate(rows):
        y = y0 + header_h + i * row_h
        bg = "#F4F1EB" if i % 2 == 0 else "#FCFBF8"
        for j, (x, w, text_value) in enumerate(zip(x_positions, widths, row)):
            lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{row_h}" fill="{bg}" stroke="#DDD9D1"/>')
            if j == 0:
                color = COLORS[["CHANEL", "Louis Vuitton", "Dior", "Hermès"][i]]
                lines.append(f'<rect x="{x}" y="{y}" width="8" height="{row_h}" fill="{color}"/>')
                lines.append(f'<text x="{x+22}" y="{y+48}" class="section">{esc(text_value)}</text>')
            else:
                words = text_value.split("；")
                for k, piece in enumerate(words):
                    lines.append(f'<text x="{x+16}" y="{y+34+k*30}" class="label">{esc(piece)}{"；" if k < len(words)-1 else ""}</text>')
    lines.append('<text x="50" y="930" class="note">最强可比证据：Chanel France 选定同款连续历史、Louis Vuitton 部分同款连续历史；Dior 与 Hermès 主要承担方向性或当前结构比较。</text>')
    lines.append('<text x="50" y="956" class="note">主读法：四个品牌并非同一种“奢侈品涨价”模型；当前梯形与历史路径的组合，决定了不同的竞争重叠区间。</text>')
    lines.append('<text x="50" y="982" class="note">边界：所有结论均为公开标价样本的外部观察，不推断管理层意图，也不推断需求、支付意愿或利润。</text>')
    save("05_four_brand_archetype_matrix.svg", lines)


if __name__ == "__main__":
    chart_current_architecture()
    chart_band_battleground()
    chart_chanel_ladder()
    chart_historical_icon_access()
    chart_archetype_matrix()
    print(f"Wrote chart assets to {OUT}")
