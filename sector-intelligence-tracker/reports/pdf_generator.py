"""
reports/pdf_generator.py
-------------------------
PDF report generation for the Sector Intelligence Tracker.
Uses fpdf2 exclusively — no reportlab, no weasyprint.
"""

from __future__ import annotations

import os
import io
import datetime
import tempfile
from pathlib import Path

import pandas as pd
from fpdf import FPDF, XPos, YPos
from data.sector_meta import SECTOR_META
from data.company_profiles import COMPANY_PROFILES

def sanitize(text: str) -> str:
    """Sanitize strings for fpdf2 to avoid latin-1 encoding errors."""
    if not isinstance(text, str):
        text = str(text)
    text = text.replace("—", "-").replace("–", "-").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return text.encode("latin-1", "replace").decode("latin-1")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ACCENT      = (55, 138, 221)   # #378ADD
DARK        = (25, 28, 30)     # #191C1E
GREY        = (113, 119, 131)  # #717783
LIGHT_BG    = (247, 249, 251)  # #F7F9FB
WHITE       = (255, 255, 255)
LIGHT_BLUE  = (219, 235, 252)  # light accent fill
DIVIDER     = (224, 227, 229)  # #E0E3E5

AUTHOR_NAME = "Mrinmoy Banikya"
PAGE_W      = 210  # A4 width mm
PAGE_H      = 297  # A4 height mm
MARGIN      = 20


# ---------------------------------------------------------------------------
# Report class
# ---------------------------------------------------------------------------

class SectorReport(FPDF):
    """Five-page sector intelligence PDF built with fpdf2."""

    def __init__(self, **kwargs):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_author(AUTHOR_NAME)
        self.set_creator("Sector Intelligence Tracker")

    # ── FPDF overrides ────────────────────────────────────────

    def header(self):
        """Minimal header — only on pages 2+."""
        if self.page_no() <= 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, "Sector Intelligence Tracker", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        self.cell(0, 6, f"Page {self.page_no()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.set_draw_color(*DIVIDER)
        self.line(MARGIN, self.get_y(), PAGE_W - MARGIN, self.get_y())
        self.ln(4)

    def footer(self):
        """Subtle footer on every page."""
        self.set_y(-15)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*GREY)
        self.cell(0, 8, f"© {datetime.datetime.now().year} {AUTHOR_NAME} · Bangalore",
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        self.cell(0, 8, f"{self.page_no()} / {{nb}}",
                  new_x=XPos.LMARGIN, new_y=YPos.TOP, align="R")

    # ── Reusable helpers ──────────────────────────────────────

    def _section_title(self, text: str):
        """Render a prominent section heading with an accent underline."""
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*DARK)
        self.cell(0, 12, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.8)
        self.line(MARGIN, self.get_y(), MARGIN + 55, self.get_y())
        self.set_line_width(0.2)
        self.ln(8)

    def _body_text(self, text: str, size: int = 10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*DARK)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def _table_header(self, cols: list[str], widths: list[float]):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*ACCENT)
        self.set_text_color(*WHITE)
        for label, w in zip(cols, widths):
            self.cell(w, 8, label, border=0, fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        self.ln()

    def _table_row(self, values: list[str], widths: list[float],
                   bold: bool = False, stripe: bool = False):
        self.set_font("Helvetica", "B" if bold else "", 9)
        self.set_text_color(*DARK)
        if stripe:
            self.set_fill_color(*LIGHT_BG)
        else:
            self.set_fill_color(*WHITE)
        for val, w in zip(values, widths):
            self.cell(w, 7, str(val), border=0, fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        self.ln()

    def _bullet(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.cell(6, 6, chr(149), new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
        self.multi_cell(0, 6, text)
        self.ln(2)

    def _kv_row(self, key: str, value: str):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREY)
        self.cell(40, 6, key, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 6, str(value))
        self.ln(1)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_report(
    sector_name: str,
    company_name: str,
    df_ratings: pd.DataFrame | dict,
    df_hiring: dict,
    df_news: dict,
    df_glassdoor: dict,
    insight_text: str,
    personalised_line_1: str = "",
    personalised_line_2: str = "",
    meta: dict = None,
) -> bytes:
    """
    Build a 5-page Sector Intelligence PDF and return raw bytes.

    Parameters
    ----------
    sector_name : str
        Sector label (e.g. "Fintech Payments").
    company_name : str
        Target company the report is prepared for.
    df_ratings : dict
        ``{company: {"rating": float, "num_ratings": int}}``.
    df_hiring : dict
        ``{company: job_count}``.
    df_news : dict
        ``{company: mention_count}``.
    df_glassdoor : dict
        ``{company: employer_score}``.
    insight_text : str
        Sector momentum narrative.
    personalised_line_1 : str
        First personalisation line.
    personalised_line_2 : str
        Second personalisation line.

    Returns
    -------
    bytes
        Raw PDF bytes.
    """
    pdf = SectorReport()
    pdf.alias_nb_pages()
    today = datetime.datetime.now().strftime("%B %d, %Y")

    # Normalise ratings to dict if DataFrame passed
    if isinstance(df_ratings, pd.DataFrame):
        ratings = {}
        for _, row in df_ratings.iterrows():
            ratings[row.get("Company", row.get("company", ""))] = {
                "rating": float(row.get("Rating", row.get("rating", 0))),
                "num_ratings": int(row.get("Reviews", row.get("num_ratings", row.get("ratings_count", 0)))),
            }
    else:
        ratings = df_ratings or {}

    hiring  = df_hiring or {}
    news    = df_news or {}
    glassdoor = df_glassdoor or {}

    # ── PAGE 1 — Cover ────────────────────────────────────────
    pdf.add_page()
    pdf.ln(55)

    # Accent line
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1.2)
    pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(12)

    # Title
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 16, "Sector Intelligence", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 16, "Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    # Sector name in accent
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 12, sector_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    # Prepared for
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 8, f"Prepared for: {company_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    # Date
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, today, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(25)

    # Footer line
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1.2)
    pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 6, f"Built by {AUTHOR_NAME} - Bangalore",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ── PAGE 2 — Market Intelligence ───────────────────────────
    pdf.add_page()
    pdf._section_title(sanitize("Market Intelligence"))

    meta_dict = meta or {}
    pdf.set_font("Helvetica", "B", 9)
    # KPI grid
    pdf.set_fill_color(*LIGHT_BG)
    pdf.cell((PAGE_W - 2 * MARGIN) / 2, 10, sanitize(f"Total Addressable Market: ${meta_dict.get('tam_usd_bn','N/A')}Bn"), border=0, fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell((PAGE_W - 2 * MARGIN) / 2, 10, sanitize(f"CAGR (5yr): {meta_dict.get('cagr_pct','N/A')}%"), border=0, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.cell((PAGE_W - 2 * MARGIN) / 2, 10, sanitize(f"Market Stage: {meta_dict.get('market_stage','N/A')}"), border=0, fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell((PAGE_W - 2 * MARGIN) / 2, 10, sanitize(f"Saturation: {meta_dict.get('saturation_score','N/A')}/100"), border=0, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)
    pdf._section_title(sanitize("Key Tailwinds"))
    for t in meta_dict.get("key_tailwinds", []):
        pdf._bullet(sanitize(t))

    pdf.ln(4)
    pdf._section_title(sanitize("Unsolved Problems (Market Gaps)"))
    for p in meta_dict.get("unsolved_problems", []):
        pdf._bullet(sanitize(p))

    pdf.ln(4)
    pdf._section_title(sanitize("Community Signals (Reddit)"))
    for r in meta_dict.get("reddit_pain_points", []):
        x, y = pdf.get_x(), pdf.get_y()
        pdf.set_draw_color(255, 69, 0)
        pdf.set_line_width(1.5)
        pdf.line(x+4, y, x+4, y+10)
        pdf.set_xy(x+8, y)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(139, 148, 158)
        pdf.multi_cell(0, 5, sanitize(r))
        pdf.set_text_color(*DARK)
        pdf.ln(2)

    # ── PAGE 3 — Sector Player Map ───────────────────────────
    pdf.add_page()
    pdf._section_title(sanitize("Sector Player Map"))
    pdf._body_text(sanitize(f"All known players in {sector_name} organized by scale and stage."))

    for tier_key, tier_label in [
        ("public_companies", "Public Companies"),
        ("private_giants", "Private Giants (>$500M valuation)"),
        ("rising_startups", "Rising Startups (<$500M valuation)"),
    ]:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*ACCENT)
        pdf.cell(0, 7, sanitize(tier_label), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(*DARK)
        
        players = meta_dict.get("players", {}).get(tier_key, [])
        pdf._table_header(["Company", "Valuation / Mkt Cap", "Stage", "HQ"], [65, 45, 40, 24])
        for p in players:
            val = f"${p['valuation_usd_bn']}Bn" if p.get('valuation_usd_bn') else "Undisclosed"
            pdf._table_row([
                sanitize(p['name']),
                sanitize(val),
                sanitize(p.get('stage','N/A')),
                sanitize(p.get('hq','N/A')),
            ], [65, 45, 40, 24])
        pdf.ln(6)

    # ── PAGE 4 — Target Company Deep-Dive ────────────────────
    pdf.add_page()
    profile = COMPANY_PROFILES.get(company_name, {})
    pdf._section_title(sanitize(f"Company Deep-Dive: {company_name}"))

    pdf.set_font("Helvetica", "", 9)
    pdf._kv_row("Founded", sanitize(str(profile.get('founded','N/A'))))
    pdf._kv_row("Valuation", sanitize(f"${profile.get('valuation_usd_bn','N/A')}Bn"))
    pdf._kv_row("Last Round", sanitize(f"{profile.get('last_round','N/A')} - ${profile.get('last_round_amount_usd_m','N/A')}M ({profile.get('last_round_year','')})"))
    pdf._kv_row("Employees", sanitize(f"~{profile.get('employee_count_approx','N/A')}"))
    pdf._kv_row("ICP", sanitize(profile.get('icp','N/A')))
    pdf._kv_row("Revenue Model", sanitize(profile.get('revenue_model','N/A')))
    pdf._kv_row("Competitive Moat", sanitize(profile.get('competitive_moat','N/A')))

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, sanitize("Known Strategic Gaps"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for gap in profile.get('known_gaps', []):
        pdf._bullet(sanitize(gap))

    # ── PAGE 5 — Brand Momentum ───────────────────────────────
    pdf.add_page()
    pdf._section_title("Brand Momentum - Google Trends 12 Months")

    # Try to embed a Plotly trends chart as PNG
    chart_embedded = False
    if news:  # use news as proxy; real trends chart below
        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            fig = go.Figure()
            companies_list = list(news.keys())
            colors = ["#378ADD", "#1D9E75", "#D85A30", "#7F77DD", "#BA7517", "#D4537E"]
            for i, company in enumerate(companies_list):
                score = news.get(company, 0)
                fig.add_trace(go.Bar(
                    x=[company], y=[score],
                    name=company,
                    marker_color=colors[i % len(colors)],
                ))
            fig.update_layout(
                title=None, barmode="group",
                font=dict(family="Arial", size=11),
                paper_bgcolor="white", plot_bgcolor="white",
                width=700, height=320,
                margin=dict(l=50, r=30, t=20, b=50),
                showlegend=False,
                yaxis=dict(showgrid=True, gridcolor="#F0F2F4"),
                xaxis=dict(showgrid=False),
            )
            tmp_path = os.path.join(tempfile.gettempdir(), "temp_trends.png")
            pio.write_image(fig, tmp_path, scale=2)
            pdf.image(tmp_path, x=MARGIN, w=PAGE_W - 2 * MARGIN)
            chart_embedded = True
        except Exception:
            pass

    if not chart_embedded:
        pdf._body_text("[Chart unavailable - install kaleido for Plotly image export]")

    pdf.ln(6)
    # Explanation
    if news:
        sorted_news = sorted(news.items(), key=lambda x: x[1], reverse=True)
        leader = sorted_news[0][0]
        pdf._body_text(
            f"{leader} leads brand momentum in the {sector_name} sector "
            f"with the highest search interest over the past 12 months. "
            f"The remaining players show varying degrees of brand visibility, "
            f"indicating opportunities for differentiated positioning."
        )
    else:
        pdf._body_text("Brand momentum data is currently unavailable for this sector.")

    # ── PAGE 3 — Product Experience ───────────────────────────
    pdf.add_page()
    pdf._section_title("App Store Ratings")

    if ratings:
        col_w = [(PAGE_W - 2 * MARGIN) * r for r in (0.40, 0.30, 0.30)]
        pdf._table_header(["Company", "Rating", "Num Ratings"], col_w)

        best_company = max(ratings, key=lambda c: ratings[c].get("rating", 0))
        for idx, (company, data) in enumerate(ratings.items()):
            is_best = company == best_company
            pdf._table_row(
                [company, f"{data.get('rating', 0):.1f}", f"{data.get('num_ratings', 0):,}"],
                col_w, bold=is_best, stripe=(idx % 2 == 1),
            )

        pdf.ln(6)
        best_r = ratings[best_company]["rating"]
        pdf._body_text(
            f"[*] {best_company} leads with a {best_r:.1f} rating on the Google Play Store, "
            f"reflecting strong product-market fit and user satisfaction."
        )
    else:
        pdf._body_text("No Play Store app data available for this sector.")

    # ── PAGE 4 — Talent Signals ───────────────────────────────
    pdf.add_page()
    pdf._section_title("Hiring Velocity + Employer Score")

    if hiring or glassdoor:
        all_companies = sorted(set(list(hiring.keys()) + list(glassdoor.keys())))
        col_w = [(PAGE_W - 2 * MARGIN) * r for r in (0.40, 0.30, 0.30)]
        pdf._table_header(["Company", "Open Roles", "Employer Score"], col_w)

        top_hiring_co = max(hiring, key=hiring.get) if hiring else None
        for idx, company in enumerate(all_companies):
            is_top = company == top_hiring_co
            pdf._table_row(
                [company, str(hiring.get(company, 0)), f"{glassdoor.get(company, 3.5):.1f}"],
                col_w, bold=is_top, stripe=(idx % 2 == 1),
            )

        pdf.ln(6)
        if top_hiring_co:
            pdf._body_text(
                f">> {top_hiring_co} leads hiring velocity with "
                f"{hiring[top_hiring_co]} open roles, signalling aggressive growth plans."
            )
    else:
        pdf._body_text("Hiring and employer data unavailable for this sector.")

    # ── PAGE 5 — Key Insights + Personalisation ───────────────
    pdf.add_page()
    pdf._section_title("3 Key Insights")

    # Insight 1: Highest hiring vs sector avg
    if hiring:
        top_h = max(hiring, key=hiring.get)
        top_h_val = hiring[top_h]
        avg_h = sum(hiring.values()) / len(hiring) if hiring else 0
        pct_diff = ((top_h_val - avg_h) / avg_h * 100) if avg_h > 0 else 0
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*DARK)
        pdf.cell(8, 7, "1.", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6,
            f"{top_h} is hiring {pct_diff:+.0f}% above the sector average "
            f"({top_h_val} roles vs {avg_h:.0f} avg), indicating aggressive expansion.")
        pdf.ln(4)
    else:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK)
        pdf.cell(0, 7, "1. Hiring data unavailable.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

    # Insight 2: Highest brand momentum
    if news:
        top_n = max(news, key=news.get)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(8, 7, "2.", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6,
            f"{top_n} dominates brand momentum with {news[top_n]} news mentions "
            f"in the past 30 days - highest in the {sector_name} cohort.")
        pdf.ln(4)
    else:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, "2. Brand momentum data unavailable.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

    # Insight 3: Best vs worst app rating
    if ratings:
        best_c = max(ratings, key=lambda c: ratings[c].get("rating", 0))
        worst_c = min(ratings, key=lambda c: ratings[c].get("rating", 0))
        best_v = ratings[best_c]["rating"]
        worst_v = ratings[worst_c]["rating"]
        gap = best_v - worst_v
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(8, 7, "3.", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6,
            f"{best_c} ({best_v:.1f}/5) leads app ratings while "
            f"{worst_c} ({worst_v:.1f}/5) trails - a {gap:.1f}-point gap "
            f"reflecting divergent product experiences.")
        pdf.ln(4)
    else:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, "3. App rating data unavailable.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

    # Divider
    pdf.ln(6)
    pdf.set_draw_color(*DIVIDER)
    pdf.set_line_width(0.5)
    pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(8)

    # Personalised section — blue box
    if personalised_line_1 or personalised_line_2:
        box_x = MARGIN
        box_y = pdf.get_y()
        box_w = PAGE_W - 2 * MARGIN
        # Calculate height needed
        pdf.set_font("Helvetica", "B", 11)
        lines = 3  # title + up to 2 personalisation lines
        box_h = 12 + lines * 8

        # Draw blue box
        pdf.set_fill_color(*LIGHT_BLUE)
        pdf.set_draw_color(*ACCENT)
        pdf.rect(box_x, box_y, box_w, box_h, style="DF")

        # Content
        pdf.set_xy(box_x + 6, box_y + 5)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*ACCENT)
        pdf.cell(0, 7, "Personalised Insight", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(box_x + 6)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK)
        if personalised_line_1:
            pdf.multi_cell(box_w - 12, 6, personalised_line_1)
        if personalised_line_2:
            pdf.set_x(box_x + 6)
            pdf.multi_cell(box_w - 12, 6, personalised_line_2)

        pdf.set_y(box_y + box_h + 8)

    # Footer watermark
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 6, f"Sector Intelligence Tracker | Built by {AUTHOR_NAME}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# File saver
# ---------------------------------------------------------------------------

def save_report(bytes_data: bytes, filename: str) -> str:
    """
    Save PDF bytes to reports/output/{filename}.pdf.

    Parameters
    ----------
    bytes_data : bytes
        Raw PDF content from ``generate_report``.
    filename : str
        Stem name (without extension).

    Returns
    -------
    str
        Absolute path to the saved file.
    """
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"{filename}.pdf"
    filepath.write_bytes(bytes_data)
    return str(filepath)
