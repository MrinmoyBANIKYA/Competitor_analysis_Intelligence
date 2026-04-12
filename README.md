# 🚀 Sector Intelligence Tracker

**A modern, AI-powered competitive intelligence platform built with Streamlit, NixTio design system, and advanced data scraping techniques.**

## ✨ Features

- **Modern NixTio Design**: Premium dark theme with glassmorphism, smooth animations, and authentic UI/UX.
- **Multi-Source Data Aggregation**:
  - 📊 **Google Trends**: Real-time sector interest tracking.
  - ⭐ **Play Store**: App ratings and user sentiment.
  - 💼 **LinkedIn**: Hiring trends and job market demand.
  - 🏢 **AmbitionBox**: Employee reviews and employer ratings.
  - 📰 **News API**: Media mentions and industry buzz.
- **AI-Powered Insights**: Generates deep sector analysis and personalized recommendations using Gemini AI.
- **PDF Report Generation**: Professional, multi-page PDF reports with charts and analytics.
- **Advanced Visualizations**: Interactive charts using Plotly with hover effects and animations.
- **Simple Authentication**: Secure login system with session management.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **UI/UX**: NixTio Design System, Custom CSS Animations
- **Data Scraping**: BeautifulSoup, Selenium, Playwright
- **AI/ML**: Google Gemini API
- **PDF Generation**: fpdf2
- **Data Processing**: Pandas
- **Charts**: Plotly

## 📂 Project Structure

```
sector-intelligence-tracker/
├── .streamlit/              # Streamlit configuration
│   └── secrets.toml          # API Keys (NEWS_API_KEY)
├── data/                     # Data scraping modules
│   ├── scrapers.py           # All data scraping logic
│   └── sectors.py            # Sector definitions and constants
├── reports/                  # Report generation
│   └── pdf_generator.py      # PDF report builder
├── utils/                    # Utility functions
│   └── helpers.py            # Formatting and helper functions
├── app.py                    # Main Streamlit application
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sector-intelligence-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   Create a `.streamlit/secrets.toml` file in the project root and add your API keys:
   ```toml
   NEWS_API_KEY = "your_news_api_key_here"
   ```

## 🏃‍♂️ Running the App

Start the Streamlit application from your terminal:

```bash
streamlit run app.py
```

The app will open automatically in your web browser.

## 📝 Usage

1. **Login**
   - Enter your credentials to access the dashboard.

2. **Select Sector**
   - Choose a sector from the sidebar (e.g., Fintech, E-commerce).

3. **View Dashboard**
   - Analyze Play Store ratings, Google Trends, hiring data, and news mentions.
   - View AI-generated insights and recommendations.

4. **Generate Report**
   - Click the "Generate PDF Report" button to create a professional PDF.
   - The report includes:
     - Cover page with sector details
     - Executive summary
     - Data visualizations
     - AI-powered analysis
     - Personalised recommendations

## 📊 Data Sources

| Source | Data Provided | Update Frequency |
|--------|---------------|------------------|
| Play Store | App ratings, reviews | Real-time |
| Google Trends | Sector interest index | Daily |
| LinkedIn | Job postings, hiring trends | Daily |
| AmbitionBox | Employer ratings, reviews | Daily |
| News API | Media mentions, articles | Real-time |

## 🎨 Design System

The app uses the **NixTio design system** with the following characteristics:

- **Dark Theme**: Deep charcoal and navy backgrounds
- **Glassmorphism**: Frosted glass effect on cards and containers
- **Vibrant Accents**: Purple (#B388FF) and Cyan (#378ADD) highlights
- **Smooth Animations**: Fade-in, slide-up, and hover effects
- **Modern Typography**: Inter and Manrope fonts

## 🤖 AI Integration

The app uses Google Gemini to generate:

- **Sector Momentum Analysis**: Interprets trends and provides strategic insights
- **Personalised Recommendations**: Tailored advice based on sector dynamics
- **Executive Summary**: Quick overview of key findings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions, please open an issue in the repository.

## 👨‍💻 Author

**Mrinmoy Banikya**

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing dashboard framework
- [NixTio Design System](https://github.com/nix-community/nix-tui/blob/main/docs/design-system.md) - For the premium UI design
- [Google Gemini API](https://ai.google.dev/) - For AI-powered insights
- [fpdf2](https://github.com/PyFPDF/fpdf2) - For PDF generation

---

**Built with ❤️ for competitive intelligence and data-driven decision making**