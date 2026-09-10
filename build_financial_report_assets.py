from __future__ import annotations

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "final_report_assets"
CALC = ROOT / "financial_business_performance" / "calculations"
FONT = "'Noto Sans CJK SC','PingFang SC','Heiti SC','Arial',sans-serif"
COLORS = {
    "chanel": "#171717",
    "fcf": "#B07A3D",
    "capex": "#7D2947",
    "brand": "#426B69",
    "hermes": "#8C4A24",
    "lvmh": "#345B8A",
}


def esc(value):
    return html.escape(str(value), quote=True)


def read_csv(name):
    with (CALC / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def number(value):
    if value in (None, ""):
        return None
    return float(value)


def fmt(value, suffix=""):
    if value is None:
        return "—"
    if abs(float(value) - round(float(value))) < 0.05:
        return f"{int(round(float(value)))}{suffix}"
    return f"{float(value):.1f}{suffix}"


def start(width, height, title, subtitle):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#FCFBF8"/>',
        f'''<style>
          .title {{ font-family:{FONT}; font-size:28px; font-weight:700; fill:#1F2933; }}
          .subtitle {{ font-family:{FONT}; font-size:15px; fill:#5B6570; }}
          .section {{ font-family:{FONT}; font-size:18px; font-weight:700; fill:#1F2933; }}
          .label {{ font-family:{FONT}; font-size:13px; fill:#39424E; }}
          .small {{ font-family:{FONT}; font-size:12px; fill:#65717C; }}
          .note {{ font-family:{FONT}; font-size:12px; fill:#66727C; }}
          .value {{ font-family:{FONT}; font-size:13px; font-weight:700; fill:#25313B; }}
          .grid {{ stroke:#D8D5CF; stroke-width:1; }}
          .axis {{ stroke:#8D959C; stroke-width:1.2; }}
        </style>''',
        f'<text x="56" y="52" class="title">{esc(title)}</text>',
        f'<text x="56" y="79" class="subtitle">{esc(subtitle)}</text>',
    ]


def finish(lines):
    lines.append("</svg>")
    return "\n".join(lines)


def save(name, lines):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(finish(lines), encoding="utf-8")


def line_panel(lines, title, rows, series, x, y, width, height, lo, hi, suffix="", decimals=0):
    lines.append(f'<text x="{x}" y="{y}" class="section">{esc(title)}</text>')
    plot_x = x + 210
    plot_y = y + 24
    plot_w = width - 240
    plot_h = height - 66
    for tick in range(int(lo), int(hi) + 1, max(1, int((hi - lo) / 4))):
        yy = plot_y + plot_h - (tick - lo) / (hi - lo) * plot_h
        lines.append(f'<line x1="{plot_x}" y1="{yy:.1f}" x2="{plot_x+plot_w}" y2="{yy:.1f}" class="grid"/>')
        lines.append(f'<text x="{plot_x-12}" y="{yy+4:.1f}" text-anchor="end" class="small">{tick}{suffix}</text>')
    if not rows:
        return
    step = plot_w / max(1, len(rows) - 1)
    for i, row in enumerate(rows):
        xx = plot_x + i * step
        lines.append(f'<line x1="{xx:.1f}" y1="{plot_y+plot_h}" x2="{xx:.1f}" y2="{plot_y+plot_h+6}" class="axis"/>')
        lines.append(f'<text x="{xx:.1f}" y="{plot_y+plot_h+24}" text-anchor="middle" class="small">{esc(row["fiscal_year"])}</text>')
    for label, field, color in series:
        points = []
        for i, row in enumerate(rows):
            val = number(row.get(field))
            if val is None:
                continue
            xx = plot_x + i * step
            yy = plot_y + plot_h - (val - lo) / (hi - lo) * plot_h
            points.append((xx, yy, val))
        if not points:
            continue
        path = " ".join(("M" if i == 0 else "L") + f"{xx:.1f},{yy:.1f}" for i, (xx, yy, _) in enumerate(points))
        lines.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3.5"/>')
        for xx, yy, val in points:
            lines.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="5" fill="#FCFBF8" stroke="{color}" stroke-width="3"/>')
        legend_x = x + 8 + sum(138 for _ in range(series.index((label, field, color))))
        legend_y = y + height - 8
        lines.append(f'<line x1="{legend_x}" y1="{legend_y-4}" x2="{legend_x+22}" y2="{legend_y-4}" stroke="{color}" stroke-width="3.5"/>')
        lines.append(f'<text x="{legend_x+28}" y="{legend_y}" class="small">{esc(label)}</text>')


def financial_performance_chart():
    rows = [row for row in read_csv("chanel_annual_performance.csv") if 2020 <= int(row["fiscal_year"]) <= 2025]
    indexed = []
    base = number(rows[0]["revenue_usd_m"])
    for row in rows:
        copy = dict(row)
        copy["revenue_index"] = None if base in (None, 0) else number(row["revenue_usd_m"]) / base * 100
        indexed.append(copy)
    lines = start(1600, 1120, "Chanel 经营表现与再投资强度", "FY2020–FY2025；指数仅作 Chanel 内部序列，百分比图不与价格共轴，也不表达因果关系。")
    line_panel(lines, "Chanel consolidated revenue index (2020 = 100)", indexed, [("Revenue (USD)", "revenue_index", COLORS["chanel"])], 80, 135, 1420, 250, 80, 210, "", 0)
    line_panel(lines, "Operating margin and FCF margin", rows, [("Operating margin", "operating_margin_pct", COLORS["chanel"]), ("FCF margin", "fcf_margin_pct", COLORS["fcf"])], 80, 435, 1420, 250, 0, 35, "%", 1)
    line_panel(lines, "Investment intensity", rows, [("Capex / revenue", "capex_revenue_pct", COLORS["capex"]), ("Brand support / revenue", "brand_support_revenue_pct", COLORS["brand"])], 80, 735, 1420, 250, 0, 18, "%", 1)
    lines.append('<line x1="56" y1="1030" x2="1544" y2="1030" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="1060" class="note">读法：2024 的收入、经营利润与 FCF 承压，但 capex / revenue 与 brand-support / revenue 仍处高位；2025 FCF 恢复，同时 capex 保持高位。所有数值为 Chanel Limited consolidated company，非手袋单项。</text>')
    lines.append('<text x="56" y="1083" class="note">来源：financial_business_performance/calculations/chanel_annual_performance.csv；2020 受 FY2021 SaaS 会计政策变更影响的 KPI 使用官方重述口径。</text>')
    save("06_chanel_financial_performance.svg", lines)


def benchmark_chart():
    hermes = read_csv("hermes_benchmark.csv")
    lvmh = read_csv("lvmh_fashion_leather_goods.csv")
    rows = []
    for h, l in zip(hermes, lvmh):
        rows.append({
            "fiscal_year": h["fiscal_year"],
            "hermes_leather_growth": h["leather_goods_saddlery_constant_currency_growth_pct"],
            "lvmh_flg_growth": l["fashion_leather_goods_organic_growth_pct"],
            "hermes_margin": h["group_recurring_operating_margin_pct"],
            "lvmh_margin": l["fashion_leather_goods_recurring_operating_margin_pct"],
        })
    lines = start(1600, 970, "Leather-goods benchmark trajectory", "Hermès Leather Goods & Saddlery 与 LVMH Fashion & Leather Goods；分别保留公司 / segment grain 与 constant-currency / organic 口径。")
    line_panel(lines, "Constant-currency / organic growth", rows, [("Hermès Leather Goods & Saddlery", "hermes_leather_growth", COLORS["hermes"]), ("LVMH Fashion & Leather Goods", "lvmh_flg_growth", COLORS["lvmh"])], 80, 135, 1420, 300, -10, 55, "%", 1)
    line_panel(lines, "Operating margin context", rows, [("Hermès group recurring margin", "hermes_margin", COLORS["hermes"]), ("LVMH F&LG recurring margin", "lvmh_margin", COLORS["lvmh"])], 80, 505, 1420, 300, 25, 45, "%", 1)
    lines.append('<line x1="56" y1="880" x2="1544" y2="880" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="910" class="note">读法：Hermès Leather Goods &amp; Saddlery 的增速在 2020 低点后持续为正；LVMH F&amp;LG 在 2024–2025 进入负增长环境。两者不是同一 reporting grain，不做绝对收入排名。</text>')
    lines.append('<text x="56" y="933" class="note">LVMH Fashion &amp; Leather Goods 是多品牌 business group，不能当作 Louis Vuitton 或 Dior 独立财务数据；Hermès métier 也不等于 handbags-only。</text>')
    save("07_luxury_benchmark_trajectory.svg", lines)


def tension_matrix_chart():
    tensions = [
        ("Exclusivity vs Recruitment", "Visible entry threshold is elevated", "Conversion / entry barrier effect is not observed", "Monitor entry coverage with internal client and migration data"),
        ("Icon Monetization vs Ladder Continuity", "Classic / icon sits above a large visible step", "Portfolio continuity risk is a question, not a finding", "Manage the whole ladder, not only the anchor"),
        ("Broad Repricing vs Competitive Substitution", "Lower/core tiers overlap different competitor battlegrounds", "Substitution cannot be inferred from list prices", "Benchmark by tier and market"),
        ("Premiumization vs Growth Quality", "Prices persist while 2024 consolidated performance weakened", "Cycle, mix, region, FX and investment confound interpretation", "Evaluate price with growth quality and cash"),
        ("Price Elevation vs Reinvestment", "Brand support and capex remain material; 2024 capex was a record", "Investment is company-wide and not handbag causal proof", "Treat desirability, experience, craftsmanship and cash as a linked management agenda"),
    ]
    lines = start(1600, 1080, "Strategic tensions: what the evidence supports", "Evidence-backed tensions for management attention; the final column is an implication / validation agenda, not a causal prescription.")
    x = [60, 350, 740, 1110]
    widths = [270, 370, 350, 430]
    headers = ["Tension", "Observed evidence", "Boundary / not proven", "Strategic implication"]
    y0 = 135
    for xx, header in zip(x, headers):
        lines.append(f'<text x="{xx}" y="{y0}" class="section">{esc(header)}</text>')
    for index, row in enumerate(tensions):
        y = y0 + 55 + index * 160
        fill = "#F1EEE8" if index % 2 == 0 else "#FCFBF8"
        lines.append(f'<rect x="48" y="{y-34}" width="1504" height="132" rx="8" fill="{fill}" stroke="#E0DDD5"/>')
        for xx, width, text in zip(x, widths, row):
            words = text.split()
            lines.append(f'<text x="{xx}" y="{y}" class="label">')
            line = ""
            line_index = 0
            for word in words:
                if len(line) + len(word) + 1 > max(24, int(width / 9)):
                    lines.append(f'<tspan x="{xx}" dy="{0 if line_index == 0 else 22}">{esc(line)}</tspan>')
                    line = word
                    line_index += 1
                else:
                    line = word if not line else line + " " + word
            if line:
                lines.append(f'<tspan x="{xx}" dy="{0 if line_index == 0 else 22}">{esc(line)}</tspan>')
            lines.append('</text>')
    lines.append('<line x1="56" y1="960" x2="1544" y2="960" stroke="#D8D5CF"/>')
    lines.append('<text x="56" y="990" class="note">证据边界：价格架构与经营数据可以共同支持战略张力；客户转化、需求弹性、销量、产品利润与 migration 需要 Chanel 内部数据。</text>')
    lines.append('<text x="56" y="1014" class="note">来源：现有 price architecture / historical panels + official Chanel, Hermès and LVMH financial sources in the structured registry。</text>')
    save("08_strategic_tension_matrix.svg", lines)


if __name__ == "__main__":
    financial_performance_chart()
    benchmark_chart()
    tension_matrix_chart()
    print("Generated 06_chanel_financial_performance.svg, 07_luxury_benchmark_trajectory.svg, 08_strategic_tension_matrix.svg")
