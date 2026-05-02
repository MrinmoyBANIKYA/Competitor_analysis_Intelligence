# NixTio — Premium Sector Intelligence Terminal

NixTio is a high-performance competitive intelligence dashboard designed for executives and strategy analysts. It compiles real-time market signals from search trends, hiring velocity, and consumer sentiment into a unified boardroom-grade interface.

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MrinmoyBANIKYA/NixTio--SectorAnalysis-.git
   cd NixTio--SectorAnalysis-
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   Create a `.streamlit/secrets.toml` file with your keys:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   NEWS_API_KEY = "your_newsapi_key"
   IS_ADMIN = true

   [credentials]
   email = "admin@nixtio.ai"
   password = "password123"
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Demo Mode**: 
   If you don't have API keys yet, simply toggle **"Demo Mode"** in the sidebar to explore the platform with pre-populated Fintech data.

## 📡 Key Features

- **AI Strategy Analyst**: Powered by Groq (Llama-3.3-70b) for real-time strategic synthesis.
- **Data Health Monitoring**: Production-grade fetcher with parallel execution and health tracking.
- **Boardroom Reports**: Export high-resolution PDF briefings with custom NixTio dark themes.
- **Glassmorphism UI**: A premium, visually immersive dashboard built for high-stakes demos.

## 🛠 Tech Stack

- **Frontend**: Streamlit, Custom CSS (NixTio Design System)
- **Data Engine**: Pandas, Concurrent Futures, Play Store Scraper, Pytrends
- **AI**: Groq API (Llama-3.3-70b-versatile)
- **Reporting**: fpdf2, Matplotlib (Dark Theme)

---
*Built by Mrinmoy Banikya*
