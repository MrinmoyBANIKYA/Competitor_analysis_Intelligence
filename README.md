# 🚀 Sector Intelligence Tracker
 
> **Live Product · CFO-Ready · Deployed**
> An AI-powered competitive intelligence platform that turns multi-source market signals into executive-grade sector reports — in minutes, not weeks.
 
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Powered by Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4?logo=google)](https://ai.google.dev)
[![Status](https://img.shields.io/badge/Status-Live%20%26%20Deployed-brightgreen)]()
 
---
 
## 🎯 The Problem
 
Every CFO, strategy team, and startup founder needs competitive intelligence. The current options are broken:
 
- **Consulting reports** cost ₹5–50 lakhs and arrive 6 weeks late
- **Manual research** takes 3–5 analyst days per sector, per quarter
- **Generic tools** (SEMrush, SimilarWeb) give digital metrics, not business signals
**There is no affordable, real-time, AI-powered competitive intelligence tool built for Indian markets.** This is that tool.
 
---
 
## ✨ What It Does
 
Sector Intelligence Tracker aggregates signals from **5 live data sources**, synthesises them with **Google Gemini AI**, and delivers a **CFO-ready PDF report** — in under 5 minutes.
 
### Live Data Sources
 
| Source | Signal | Refresh |
|--------|--------|---------|
| 📊 Google Trends | Consumer interest & search momentum | Daily |
| ⭐ Google Play Store | App ratings, user sentiment, competitor product health | Real-time |
| 💼 LinkedIn Jobs | Hiring velocity, talent demand, growth signals | Daily |
| 🏢 AmbitionBox | Employee sentiment, employer health scores | Daily |
| 📰 News API | Media mentions, PR activity, crisis signals | Real-time |
 
### AI-Powered Output
 
- **Sector Momentum Analysis**: Gemini interprets cross-source signal convergence
- **Competitor Benchmarking**: Side-by-side positioning across all data dimensions
- **Strategic Recommendations**: Tailored to your sector's current dynamics
- **Executive Summary**: One-page brief suitable for board-level consumption
### Report Generation
One click → professional multi-page PDF with:
- Cover page with sector snapshot
- Executive summary
- Interactive charts (static in PDF)
- AI analysis and recommendations
- Data methodology notes
---
 
## 🖥️ Product Demo
 
```
Login → Select Sector (e.g., Fintech / EdTech / SaaS) 
     → Dashboard loads with live multi-source data
     → View AI-generated insights in real time
     → Click "Generate Report" → Download CFO-ready PDF
```
 
The dashboard renders interactive Plotly charts with hover effects, sector comparison tables, and trend lines — all in a premium dark-theme UI built on the NixTio design system.
 
---
 
## 🛠️ Tech Stack
 
```
Frontend          Streamlit + Custom CSS (NixTio Design System)
Data Layer        BeautifulSoup · Selenium · Playwright · pytrends · News API
AI Engine         Google Gemini API (sector analysis + recommendations)
Visualisation     Plotly (interactive) · Pandas (data processing)
Report Export     fpdf2 (multi-page PDF generation)
Auth              Session-based login with Streamlit secrets
```
 
---
 
## 📁 Project Structure
 
```
sector-intelligence-tracker/
├── app.py                    # Main application entry point
├── data/
│   ├── scrapers.py           # Multi-source data aggregation layer
│   └── sectors.py            # Sector taxonomy and constants
├── reports/
│   └── pdf_generator.py      # PDF report builder
├── utils/
│   └── helpers.py            # Formatting and helper functions
└── .streamlit/
    └── secrets.toml          # API key configuration (not committed)
```
 
---
 
## 🚀 Getting Started
 
### Prerequisites
- Python 3.8+
- Google Gemini API key
- News API key
### Installation
 
```bash
git clone https://github.com/MrinmoyBANIKYA/Competitor_analysis_Intelligence.git
cd Competitor_analysis_Intelligence/sector-intelligence-tracker
 
pip install -r requirements.txt
```
 
### Configuration
 
Create `.streamlit/secrets.toml`:
```toml
NEWS_API_KEY = "your_news_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```
 
### Run
 
```bash
streamlit run app.py
```
 
---
 
## 📈 Market Opportunity & Impact Potential
 
This product sits at the intersection of three growing Indian market needs:
 
**The TAM is real:**
- 50,000+ active startups in India need competitive intelligence but can't afford consulting
- 100,000+ CFOs and strategy heads at SMEs lack real-time sector data
- VC firms and accelerators run portfolio reviews quarterly — each one is a use case
**With modest additions, this becomes a SaaS product:**
 
| Addition | Effort | Impact |
|----------|--------|--------|
| Multi-user auth + org accounts | ~2 weeks | Enables B2B subscription |
| Sector watchlist + email alerts | ~1 week | Daily active usage |
| Historical trend archival (DB) | ~2 weeks | Longitudinal analysis — high value for VCs |
| API access tier | ~3 weeks | Developer/enterprise channel |
| India-specific sources (BSE filings, MCA data) | ~3 weeks | Unmatched for Indian market |
 
**Estimated pricing model:** ₹2,999–₹9,999/month per org (5–15 reports/month). At 500 paying customers, this is a ₹2–5 Cr ARR business with near-zero variable cost.
 
---
 
## 🎨 Design Philosophy
 
The UI is built on the **NixTio design system** — a premium dark-theme framework with:
- Deep charcoal and navy base
- Glassmorphism card effects
- Purple (`#B388FF`) and Cyan (`#378ADD`) accent system
- Smooth fade-in and slide-up animations
- Inter + Manrope typography stack
The intent: when a CFO opens this dashboard, it should feel like a Bloomberg terminal, not a data science notebook.
 
---
 
## 🔭 Roadmap
 
- [ ] PostgreSQL backend for report history and trend archiving
- [ ] Multi-org SaaS authentication (Supabase or Firebase)
- [ ] Email digest scheduler (weekly sector briefing)
- [ ] India-specific data sources: BSE filings, MCA incorporation data, Tracxn signal integration
- [ ] Competitor comparison mode (head-to-head sector players)
- [ ] Mobile-optimised view
---
 
## 📄 License
 
MIT License — see [LICENSE](LICENSE) for details.
 
---
 
## 👤 Author
 
**Mrinmoy Banikya** — Builder. The gap between raw data and executive decisions is where this product lives.
 
---
 
> *"Intelligence is not about more data. It's about the right signal, synthesised fast enough to act on."*
 