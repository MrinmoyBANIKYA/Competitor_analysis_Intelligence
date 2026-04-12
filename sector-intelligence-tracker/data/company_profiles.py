COMPANY_PROFILES = {
    # ---------------- Fintech Payments ----------------
    "Razorpay": {
        "founded": 2014,
        "hq": "Bangalore",
        "founders": ["Harshil Mathur", "Shashank Kumar"],
        "valuation_usd_bn": 7.5,
        "last_round": "Series F",
        "last_round_amount_usd_m": 375,
        "last_round_year": 2021,
        "total_raised_usd_m": 816,
        "investors": ["Sequoia", "GIC", "Ribbit Capital", "Tiger Global"],
        "employee_count_approx": 3000,
        "revenue_model": "MDR on payment volume + SaaS subscriptions",
        "primary_customers": "SMEs and startups (B2B), 8M+ merchants",
        "icp": "Tech-enabled SME, 10-500 employees, monthly GMV > Rs 5L",
        "products": ["Payment Gateway", "Payroll (RazorpayX)", "Capital", "Magic Checkout"],
        "known_gaps": [
            "Consumer-facing brand nearly zero vs PhonePe/Paytm",
            "International expansion very limited vs Stripe",
            "Customer support quality widely criticized (Trustpilot 2.1/5)",
            "Profitability path unclear — heavy cash burn on RazorpayX"
        ],
        "competitive_moat": "Deep API integration + developer trust + 8M merchant lock-in",
        "threat_from": ["Cashfree (pricing)", "Stripe India entry", "ONDC disruption"],
        "twitter_handle": "Razorpay",
        "reddit_search_term": "Razorpay payment gateway",
        "leadership": [
            {
                "name": "Harshil Mathur",
                "role": "CEO & Co-founder",
                "background": "IIT Roorkee, ex-Schlumberger",
                "known_for": "Built Razorpay from a dorm room pivot to India's top payment gateway",
                "linkedin_url": "https://linkedin.com/in/harshilmathur",
                "competitive_signal": "Recently spoke on credit infra at multiple conferences — signals upcoming lending push",
                "hire_from": ["Stripe", "PayPal", "Google"]
            },
            {
                "name": "Shashank Kumar",
                "role": "Managing Director & Co-founder",
                "background": "IIT Roorkee, ex-Microsoft",
                "known_for": "Architected Razorpay's high-availability payment stack",
                "linkedin_url": "https://linkedin.com/in/shashank-kumar-6b815217",
                "competitive_signal": "Focusing on international expansion and FX products for 2024",
                "hire_from": ["Microsoft", "Oracle", "Twilio"]
            }
        ]
    },
    "PhonePe": {
        "founded": 2015,
        "hq": "Bangalore",
        "founders": ["Sameer Nigam", "Rahul Chari", "Burzin Engineer"],
        "valuation_usd_bn": 12.0,
        "last_round": "Private Equity",
        "last_round_amount_usd_m": 850,
        "last_round_year": 2023,
        "total_raised_usd_m": 2200,
        "investors": ["General Atlantic", "Walmart", "Tiger Global"],
        "employee_count_approx": 5000,
        "revenue_model": "MDR (Offline) + Bill payments + Insurance cross-sell",
        "primary_customers": "Retail consumers + offline Kirana merchants",
        "icp": "Tier 1-3 retail user making 5+ digital TXNs/month",
        "products": ["UPI Payments", "SmartSpeaker", "InsuranceBroking", "Share.Market"],
        "known_gaps": [
            "Over-reliance on UPI which has zero-MDR mandate",
            "Regulatory overhang: NPCI 30% market-share cap",
            "Lending strategy is lagging behind Paytm",
            "Cluttered UX with too many cross-sell products"
        ],
        "competitive_moat": "Unrivaled offline merchant network + 400M+ registered users",
        "threat_from": ["Google Pay", "Jio Financial Services", "Paytm revival"],
        "twitter_handle": "PhonePe",
        "reddit_search_term": "PhonePe app UPI",
        "leadership": [
            {
                "name": "Sameer Nigam",
                "role": "CEO & Co-founder",
                "background": "NIT Kurukshetra, ex-Flipkart, ex-Microsoft",
                "known_for": "Scaling PhonePe to become the #1 UPI player in India",
                "linkedin_url": "https://linkedin.com/in/sameernigam",
                "competitive_signal": "Publicly pushing for 'Share.Market' and insurance cross-sell to improve margins",
                "hire_from": ["Flipkart", "Amazon", "Acko"]
            },
            {
                "name": "Rahul Chari",
                "role": "CTO & Co-founder",
                "background": "BITS Pilani, ex-Flipkart",
                "known_for": "Built the distributed systems architecture for Flipkart and PhonePe",
                "linkedin_url": "https://linkedin.com/in/rchari",
                "competitive_signal": "Active on X (Twitter) about Account Aggregator and OCEN infra deep-dives",
                "hire_from": ["Google", "Salesforce"]
            }
        ]
    },
    "Juspay": {
        "founded": 2012,
        "hq": "Bangalore",
        "founders": ["Vimal Kumar", "Ramanathan RV"],
        "valuation_usd_bn": 0.46,
        "last_round": "Series C",
        "last_round_amount_usd_m": 60,
        "last_round_year": 2021,
        "total_raised_usd_m": 87,
        "investors": ["SoftBank", "Accel", "Wellington"],
        "employee_count_approx": 1000,
        "revenue_model": "API transaction fee (SaaS)",
        "primary_customers": "Enterprise platforms (Swiggy, Amazon, Cred)",
        "icp": "High volume enterprise processing >1M transactions/month",
        "products": ["Express Checkout", "UPI Intent", "Tokenization"],
        "known_gaps": [
            "Low awareness amongst SME merchants",
            "Reliance on third-party PAs (Payment Aggregators)",
            "Pure cost-center offering for merchants"
        ],
        "competitive_moat": "Best-in-class checkout success rates + Namma Yatri open-source play",
        "threat_from": ["Razorpay Optimizer", "Stripe Checkout"],
        "twitter_handle": "Juspay",
        "reddit_search_term": "Juspay checkout",
        "leadership": [
            {
                "name": "Vimal Kumar",
                "role": "CEO & Co-founder",
                "background": "College of Engineering Guindy, ex-Amazon",
                "known_for": "The technical force behind India's UPI 1.0 architecture and Beckn protocol",
                "linkedin_url": "https://linkedin.com/in/vimalkumar",
                "competitive_signal": "Heavy investment in 'Namma Yatri' signals move towards open mobility and hyper-local data",
                "hire_from": ["Flipkart", "Razorpay", "BrowserStack"]
            }
        ]
    },
    "BharatPe": {
        "founded": 2018,
        "hq": "Delhi",
        "founders": ["Ashneer Grover", "Shashvat Nakrani"],
        "valuation_usd_bn": 2.85,
        "last_round": "Series F",
        "last_round_amount_usd_m": 370,
        "last_round_year": 2021,
        "total_raised_usd_m": 680,
        "investors": ["Tiger Global", "Peak XV", "Steadview"],
        "employee_count_approx": 1500,
        "revenue_model": "Lending (Merchant cash advance) + Swipe machines",
        "primary_customers": "Offline SME merchants",
        "icp": "Offline merchant doing Rs 50k+ monthly QR scanning",
        "products": ["BharatSwipe", "QR Codes", "Postpe", "Merchant Loans"],
        "known_gaps": [
            "Severe leadership attrition and internal fraud controversies",
            "Postpe consumer traction has heavily stagnated",
            "High NPA risk on unsecured merchant loans"
        ],
        "competitive_moat": "Pioneered zero-MDR interoperable QR in India",
        "threat_from": ["PhonePe SmartSpeakers", "Paytm Soundbox", "Banks pushing QR"],
        "twitter_handle": "bharatpeindia",
        "reddit_search_term": "BharatPe loan",
        "leadership": [
            {
                "name": "Nalin Negi",
                "role": "CEO",
                "background": "Ex-SBI Card, ex-GE Capital",
                "known_for": "Steering SBI Card's IPO; cleaning up BharatPe's governance after founder exits",
                "linkedin_url": "https://linkedin.com/in/nalin-negi",
                "competitive_signal": "Focusing on EBITDA positivity and scaling the unsecured merchant lending book",
                "hire_from": ["SBI Card", "ICICI Bank", "American Express"]
            }
        ]
    },
    "Simpl": {
        "founded": 2015,
        "hq": "Bangalore",
        "founders": ["Nitya Sharma", "Chaitra Chidanand"],
        "valuation_usd_bn": 0.24,
        "last_round": "Series C",
        "last_round_amount_usd_m": 40,
        "last_round_year": 2021,
        "total_raised_usd_m": 83,
        "investors": ["Valar Ventures", "IA Ventures"],
        "employee_count_approx": 500,
        "revenue_model": "Merchant discount rate (MDR) + Late fees",
        "primary_customers": "D2C brands, Food delivery apps, young consumers",
        "icp": "Gen-Z / Millennial without credit card ordering food/groceries weekly",
        "products": ["1-Tap Checkout (BNPL)", "Bill Box"],
        "known_gaps": [
            "High default rates in unsecured BNPL portfolio",
            "Stricter RBI norms on digital lending crushing margins",
            "Declining random merchants blocks user accounts without warning"
        ],
        "competitive_moat": "Seamless zero-friction 1-click checkout experience",
        "threat_from": ["LazyPay", "Mobikwik Zip", "UPI Credit"],
        "twitter_handle": "getsigmp",
        "reddit_search_term": "Simpl pay later blocked",
        "leadership": [
            {
                "name": "Nitya Sharma",
                "role": "CEO & Co-founder",
                "background": "U Michigan, ex-Goldman Sachs",
                "known_for": "Pioneering 1-tap checkout BNPL experience in India",
                "linkedin_url": "https://linkedin.com/in/nityasharma",
                "competitive_signal": "Pivot towards D2C checkout network (Simpl Checkout) to reduce dependency on BNPL interest",
                "hire_from": ["Uber", "Zomato", "Swiggy"]
            }
        ]
    },
    "Scapia": {
        "founded": 2023,
        "hq": "Bangalore",
        "founders": ["Anil Goteti"],
        "valuation_usd_bn": 0.1,
        "last_round": "Series A",
        "last_round_amount_usd_m": 23,
        "last_round_year": 2023,
        "total_raised_usd_m": 32,
        "investors": ["Elevation Capital", "3one4 Capital"],
        "employee_count_approx": 100,
        "revenue_model": "Interchange fees + Forex markup + Travel bookings",
        "primary_customers": "Frequent travelers, Millennials",
        "icp": "Salaried professional (Rs 12L+ PA) seeking zero-forex travel rewards",
        "products": ["Co-branded Credit Card", "In-app Travel Booking"],
        "known_gaps": [
            "Highly dependent on Federal Bank partnership",
            "RBI crackdown on co-branded cards limiting growth",
            "Flight booking prices in-app often higher than direct"
        ],
        "competitive_moat": "Zero-forex markup + intuitive travel-reward coin system",
        "threat_from": ["Niyo Global", "HDFC Regalia", "Uni Cards"],
        "twitter_handle": "ScapiaCards",
        "reddit_search_term": "Scapia Federal Bank credit card",
        "leadership": [
            {
                "name": "Anil Goteti",
                "role": "CEO & Founder",
                "background": "IIT Madras, ex-SVP Flipkart",
                "known_for": "Scaled Flipkart's marketplace and travel categories",
                "linkedin_url": "https://linkedin.com/in/anilgoteti",
                "competitive_signal": "Aggressively hiring travel-tech experts to build a full-stack OTA in-app",
                "hire_from": ["MakeMyTrip", "Booking.com", "Flipkart"]
            }
        ]
    },

    # ---------------- Analytics Consulting ----------------
    "MathCo": {
        "founded": 2016,
        "hq": "Bangalore",
        "founders": ["Sayandeb Banerjee", "Aditya Kumbakonam"],
        "valuation_usd_bn": None,
        "last_round": "Series A",
        "last_round_amount_usd_m": 50,
        "last_round_year": 2022,
        "total_raised_usd_m": 50,
        "investors": ["Brighton Park Capital", "Arihant Patni"],
        "employee_count_approx": 1200,
        "revenue_model": "Consulting retainers + bespoke IP licensing",
        "primary_customers": "Fortune 500 CPG and Retail",
        "icp": "Global CDO looking to build proprietary ML platforms",
        "products": ["NucliOS (Data ecosystem strategy)", "Custom ML models"],
        "known_gaps": [
            "Scaling bottleneck tied to finding niche data engineering talent",
            "Heavy reliance on a few anchor CPG clients",
            "Priced higher than traditional IT service providers"
        ],
        "competitive_moat": "Retains IP for the client (unlike typical SaaS vendors)",
        "threat_from": ["Fractal", "Mu Sigma", "Accenture Applied Intelligence"],
        "twitter_handle": "The_MathCompany",
        "reddit_search_term": "Mathco consulting interview",
        "leadership": [
            {
                "name": "Sayandeb Banerjee",
                "role": "CEO & Co-founder",
                "background": "Ex-GE Capital, ex-Mu Sigma",
                "known_for": "Scaling MathCo to one of India's fastest-growing analytics firms",
                "linkedin_url": "https://linkedin.com/in/sayandebbanerjee",
                "competitive_signal": "Focusing on 'NucliOS' to transition from services to a product-led consulting model",
                "hire_from": ["Accenture", "Deloitte", "Mu Sigma"]
            }
        ]
    },
    "Sigmoid": {
        "founded": 2013,
        "hq": "Bangalore",
        "founders": ["Lokesh Anand", "Mayur Rustagi"],
        "valuation_usd_bn": None,
        "last_round": "Series B",
        "last_round_amount_usd_m": 12,
        "last_round_year": 2022,
        "total_raised_usd_m": 19,
        "investors": ["Pharos Capital", "Peak XV"],
        "employee_count_approx": 800,
        "revenue_model": "Data engineering consulting services",
        "primary_customers": "CPG, Retail, and Ad-tech enterprises",
        "icp": "VP Data Engineering migrating legacy stacks to Databricks/Snowflake",
        "products": ["DataOps", "MLOps", "Cloud Migration"],
        "known_gaps": [
            "Highly commoditized data engineering space",
            "Lack of proprietary SaaS tooling limits margin expansion",
            "Lower brand recall compared to Fractal or Mu Sigma"
        ],
        "competitive_moat": "Deep partnerships with Snowflake and AWS",
        "threat_from": ["Tiger Analytics", "LatentView"],
        "twitter_handle": "SigmoidHQ",
        "reddit_search_term": "Sigmoid analytics work culture",
        "leadership": [
            {
                "name": "Lokesh Anand",
                "role": "CEO & Co-founder",
                "background": "IIT Kharagpur, ex-P&G",
                "known_for": "Driving Sigmoid's growth in the data engineering and MLOps space",
                "linkedin_url": "https://linkedin.com/in/lokeshanand",
                "competitive_signal": "Focusing on large-scale data migrations to Snowflake/Databricks",
                "hire_from": ["TCS", "Accenture", "Mu Sigma"]
            }
        ]
    },
    "Tiger Analytics": {
        "founded": 2011,
        "hq": "Chennai",
        "founders": ["Mahesh Kumar"],
        "valuation_usd_bn": None,
        "last_round": "Private Equity",
        "last_round_amount_usd_m": 40,
        "last_round_year": 2021,
        "total_raised_usd_m": 40,
        "investors": ["Bain Capital"],
        "employee_count_approx": 4000,
        "revenue_model": "Time & Material / Outcome-based consulting",
        "primary_customers": "Insurance, CPG, and Logistics giants",
        "icp": "Global enterprise lacking in-house advanced analytics squads",
        "products": ["Demand Forecasting", "Customer Analytics", "Computer Vision AI"],
        "known_gaps": [
            "Massive hiring sprint diluted average talent quality",
            "Becoming too large, mimicking sluggish IT services",
            "Struggling to position purely as a GenAI native firm"
        ],
        "competitive_moat": "Scale and delivery predictability in complex ML projects",
        "threat_from": ["Fractal", "TCS AI", "Infosys Topaz"],
        "twitter_handle": "TigerAnalytics",
        "reddit_search_term": "Tiger analytics data science salary",
        "leadership": [
            {
                "name": "Mahesh Kumar",
                "role": "CEO & Founder",
                "background": "IIT Bombay, Ph.D. MIT, ex-Rutgers faculty",
                "known_for": "Applying operations research and advanced math to logistics and retail problems",
                "linkedin_url": "https://linkedin.com/in/mahesh-kumar-0b8152",
                "competitive_signal": "Hiring 500+ data scientists in 2024 to support new CPG client intakes",
                "hire_from": ["Fractal", "Infosys", "IBM"]
            }
        ]
    },
    "Fractal": {
        "founded": 2000,
        "hq": "Mumbai",
        "founders": ["Srikanth Velamakanni", "Pranay Agrawal"],
        "valuation_usd_bn": 1.0,
        "last_round": "Private Equity",
        "last_round_amount_usd_m": 360,
        "last_round_year": 2022,
        "total_raised_usd_m": 685,
        "investors": ["TPG", "Apax Partners"],
        "employee_count_approx": 4500,
        "revenue_model": "Consulting + AI Product spin-offs",
        "primary_customers": "Fortune 500 across CPG, Healthcare, Tech",
        "icp": "Enterprise seeking end-to-end AI transformation",
        "products": ["Crux Intelligence", "Qure.ai", "Eugenie.ai"],
        "known_gaps": [
            "High attrition in middle management (Directors)",
            "Product portfolio often distracts from core consulting margins",
            "Delayed IPO timelines raising liquidity concerns"
        ],
        "competitive_moat": "Spinning off successful independent SaaS AI products (e.g. Qure.ai)",
        "threat_from": ["Mu Sigma", "Palantir", "MBB AI arms"],
        "twitter_handle": "FractalAnalytics",
        "reddit_search_term": "Fractal analytics interview",
        "leadership": [
            {
                "name": "Srikanth Velamakanni",
                "role": "Group CEO",
                "background": "IIT Delhi, IIM Ahmedabad, ex-ANZ",
                "known_for": "Visionary leader in the Indian analytics ecosystem for 20+ years",
                "linkedin_url": "https://linkedin.com/in/srikanthvelamakanni",
                "competitive_signal": "Pushing heavily into GenAI (Flylib) and medical AI (Qure.ai) spin-offs",
                "hire_from": ["McKInsey", "BCG", "Google"]
            }
        ]
    },
    "LatentView": {
        "founded": 2006,
        "hq": "Chennai",
        "founders": ["Venkat Viswanathan"],
        "valuation_usd_bn": 1.1,
        "last_round": "IPO",
        "last_round_amount_usd_m": 80,
        "last_round_year": 2021,
        "total_raised_usd_m": 80,
        "investors": ["Public"],
        "employee_count_approx": 1200,
        "revenue_model": "Data engineering + Business Analytics consulting",
        "primary_customers": "Tech giants (e.g. Microsoft, Adobe)",
        "icp": "Digital-native enterprise scaling product analytics",
        "products": ["SmartInsights", "MatchView"],
        "known_gaps": [
            "Overly concentrated risk in top 3 tech clients",
            "Post-IPO stock performance pressure affecting long-term investments",
            "Viewed primarily as offshore BI/Reporting rather than core AI"
        ],
        "competitive_moat": "Deep integration into Silicon Valley tech giants' data pipelines",
        "threat_from": ["EXL", "Genpact", "Tiger Analytics"],
        "twitter_handle": "LatentView",
        "reddit_search_term": "LatentView analytics stock",
        "leadership": [
            {
                "name": "Venkat Viswanathan",
                "role": "Founder & Chairman",
                "background": "IIT Madras, IIM Calcutta, ex-Cognizant",
                "known_for": "Taking one of India's first pure-play analytics firms public",
                "linkedin_url": "https://linkedin.com/in/venkatv",
                "competitive_signal": "Active on X about the impact of GenAI on offshore delivery models",
                "hire_from": ["Cognizant", "Mindtree", "Zinnov"]
            }
        ]
    },

    # ---------------- Wealthtech ----------------
    "Smallcase": {
        "founded": 2015,
        "hq": "Bangalore",
        "founders": ["Vasanth Kamath", "Anugrah Shrivastava"],
        "valuation_usd_bn": 0.2,
        "last_round": "Series C",
        "last_round_amount_usd_m": 40,
        "last_round_year": 2021,
        "total_raised_usd_m": 65,
        "investors": ["Peak XV", "Faering Capital", "Amazon"],
        "employee_count_approx": 350,
        "revenue_model": "Broker API fees + Publisher subscription cuts",
        "primary_customers": "Retail investors and SEBI RIAs",
        "icp": "Retail investor looking for direct equity portfolios (PMS alternative)",
        "products": ["Thematic Portfolios", "Publisher SaaS", "Tickertape"],
        "known_gaps": [
            "Churn rate is high after a user tries one thematic portfolio",
            "Dependent entirely on upstream broker (Zerodha/Upstox) integrations",
            "SEBI regulations on finfluencers directly hurts publisher acquisition"
        ],
        "competitive_moat": "Monopoly on thematic basket investing infrastructure in India",
        "threat_from": ["Mutual Funds", "Groww internal baskets", "WealthDesk"],
        "twitter_handle": "smallcaseHQ",
        "reddit_search_term": "Smallcase hidden charges",
        "leadership": [
            {
                "name": "Vasanth Kamath",
                "role": "CEO & Co-founder",
                "background": "IIT Kharagpur, ex-Zerodha",
                "known_for": "Building the 'Thematic basket' investing category in India",
                "linkedin_url": "https://linkedin.com/in/vasanth-kamath",
                "competitive_signal": "Pushing for 'smallcase for advisors' model to expand beyond direct retail",
                "hire_from": ["Zerodha", "Groww", "HDFC securities"]
            }
        ]
    },
    "Groww": {
        "founded": 2016,
        "hq": "Bangalore",
        "founders": ["Lalit Keshre", "Harsh Jain"],
        "valuation_usd_bn": 3.0,
        "last_round": "Series E",
        "last_round_amount_usd_m": 251,
        "last_round_year": 2021,
        "total_raised_usd_m": 393,
        "investors": ["Peak XV", "Tiger Global", "Iconiq"],
        "employee_count_approx": 1800,
        "revenue_model": "Brokerage on F&O/Equity + Mutual Fund trail (historical) + Lending",
        "primary_customers": "Gen-Z and Millennial retail investors",
        "icp": "Tier 2/3 city user making their first mutual fund SIP",
        "products": ["Mutual Funds", "Stocks", "F&O", "Groww Credit"],
        "known_gaps": [
            "Active trader toolset is far inferior to Zerodha/Upstox",
            "Recent UI glitches during market open damaged brand trust",
            "Zero brokerage on basic delivery hurts profitability requiring F&O push"
        ],
        "competitive_moat": "Incredibly simple UX leading to highest active user base in India",
        "threat_from": ["Zerodha", "Angel One", "Jio Financial"],
        "twitter_handle": "_groww",
        "reddit_search_term": "Groww app glitch",
        "leadership": [
            {
                "name": "Lalit Keshre",
                "role": "CEO & Co-founder",
                "background": "IIT Bombay, ex-Flipkart",
                "known_for": "Mastermind behind Groww's ultra-simple MF and stock investing UX",
                "linkedin_url": "https://linkedin.com/in/lalitkeshre",
                "competitive_signal": "Expanding into lending and credit to build a full-stack digital bank",
                "hire_from": ["Flipkart", "Paytm", "HDFC Bank"]
            }
        ]
    },
    "Zerodha": {
        "founded": 2010,
        "hq": "Bangalore",
        "founders": ["Nithin Kamath", "Nikhil Kamath"],
        "valuation_usd_bn": 3.6,
        "last_round": "Bootstrapped",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2024,
        "total_raised_usd_m": 0,
        "investors": [],
        "employee_count_approx": 1200,
        "revenue_model": "Flat Rs 20 on intraday/F&O + Account Opening fees",
        "primary_customers": "Active retail traders and long-term investors",
        "icp": "Serious active trader pushing high volume F&O daily",
        "products": ["Kite", "Coin", "Varsity", "Sensibull (partner)"],
        "known_gaps": [
            "Tech infrastructure hangs during extreme market volatility days",
            "No margin trading facility (MTF) unlike Angel One",
            "Strictly no-call customer support frustrates some users"
        ],
        "competitive_moat": "Stellar brand trust + totally bootstrapped high-margin cash engine",
        "threat_from": ["Groww user acquisition", "Angel One MTF", "SEBI F&O curbs"],
        "twitter_handle": "zerodhaonline",
        "reddit_search_term": "Zerodha kite disconnected",
        "leadership": [
            {
                "name": "Nithin Kamath",
                "role": "Founder & CEO",
                "background": "Bootstrapped expert",
                "known_for": "Built India's top retail brokerage without a single dollar of VC funding",
                "linkedin_url": "https://linkedin.com/in/nithinkamath",
                "competitive_signal": "Consistently critiquing high VC burn models; focusing on 'Rainmatter' climate & health startups",
                "hire_from": ["TCS", "Infosys", "Wipro"]
            }
        ]
    },
    "Ditto": {
        "founded": 2021,
        "hq": "Bangalore",
        "founders": ["Bhanu Harish Gurram", "Pawan Kumar", "Shrehith Karkera"],
        "valuation_usd_bn": None,
        "last_round": "Series A",
        "last_round_amount_usd_m": 4,
        "last_round_year": 2021,
        "total_raised_usd_m": 4,
        "investors": ["Zerodha (Rainmatter)"],
        "employee_count_approx": 300,
        "revenue_model": "Insurance broker commissions",
        "primary_customers": "Young professionals buying first term/health insurance",
        "icp": "25-35 year old worried about mis-selling via traditional agents",
        "products": ["Term Insurance Advisory", "Health Insurance Advisory"],
        "known_gaps": [
            "Cannot scale infinitely due to human-in-the-loop advisory model",
            "High reliance on Finshots media property as top funnel",
            "Vulnerable to insurance companies cutting broker commission caps"
        ],
        "competitive_moat": "Zero-spam, highly trusted advisory model in a low-trust industry",
        "threat_from": ["PolicyBazaar", "Acko (Direct to consumer)"],
        "twitter_handle": "joinditto",
        "reddit_search_term": "Ditto insurance review",
        "leadership": [
            {
                "name": "Bhanu Harish Gurram",
                "role": "Co-founder",
                "background": "IIM Ahmedabad",
                "known_for": "Building Finshots and Ditto into a content-first insurance advisory powerhouse",
                "linkedin_url": "https://linkedin.com/in/bhanuharish",
                "competitive_signal": "Hiring extensively for medical claims experts to build a claims-assistance vertical",
                "hire_from": ["TATA AIG", "HDFC Ergo", "PolicyBazaar"]
            }
        ]
    },
    "INDmoney": {
        "founded": 2019,
        "hq": "Gurugram",
        "founders": ["Ashish Kashyap"],
        "valuation_usd_bn": 0.5,
        "last_round": "Series D",
        "last_round_amount_usd_m": 86,
        "last_round_year": 2022,
        "total_raised_usd_m": 144,
        "investors": ["Tiger Global", "Steadview", "Dragoneer"],
        "employee_count_approx": 600,
        "revenue_model": "US Stock brokerage markup + Lending + Advisory fees",
        "primary_customers": "HNI and upper-middle class Millennials",
        "icp": "Tech worker wanting to invest in FAANG stocks and track net worth",
        "products": ["US Stocks", "Net Worth Tracker", "Mutual Funds"],
        "known_gaps": [
            "LRS taxation changes severely crippled the US stocks USP",
            "Data privacy concerns over continuous email scraping for net worth",
            "Customer support quality is heavily criticized"
        ],
        "competitive_moat": "Best-in-class automated net worth tracking across all asset classes",
        "threat_from": ["Vested Finance", "Groww", "Kuvera"],
        "twitter_handle": "INDmoneyApp",
        "reddit_search_term": "INDmoney email reading",
        "leadership": [
            {
                "name": "Ashish Kashyap",
                "role": "Founder & CEO",
                "background": "Ex-ibibo, ex-Google India",
                "known_for": "Serial entrepreneur who built Goibibo and redBus",
                "linkedin_url": "https://linkedin.com/in/ashishkashyap",
                "competitive_signal": "Focusing on 'Fixed Income' and 'Credit Cards' to counter US Stocks slowdown",
                "hire_from": ["Goibibo", "Paytm", "Citibank"]
            }
        ]
    },

    # ---------------- Supply Chain Tech ----------------
    "Zetwerk": {
        "founded": 2018,
        "hq": "Bangalore",
        "founders": ["Amrit Acharya", "Srinath Ramakkrushnan"],
        "valuation_usd_bn": 2.8,
        "last_round": "Series F",
        "last_round_amount_usd_m": 120,
        "last_round_year": 2023,
        "total_raised_usd_m": 670,
        "investors": ["Peak XV", "Greenoaks", "Avenir"],
        "employee_count_approx": 2000,
        "revenue_model": "B2B manufacturing marketplace take-rate",
        "primary_customers": "Global OEMs and infrastructure giants",
        "icp": "US/Europe OEM seeking China-Plus-One contract manufacturing in India",
        "products": ["Precision Parts", "Capital Goods", "Consumer Electronics Assembly"],
        "known_gaps": [
            "Heavy working capital requirements limit infinite scaling",
            "Margin profile is closer to traditional manufacturing than SaaS",
            "Geopolitical concentration risks"
        ],
        "competitive_moat": "Unmatched supplier network depth in India + stringent quality vetting",
        "threat_from": ["Moglix", "Bizongo", "Traditional EMS giants"],
        "twitter_handle": "ZetwerkHQ",
        "reddit_search_term": "Zetwerk work culture",
        "leadership": [
            {
                "name": "Amrit Acharya",
                "role": "CEO & Co-founder",
                "background": "IIT Madras, ex-McKinsey",
                "known_for": "Scaling custom manufacturing into a multi-billion dollar platform",
                "linkedin_url": "https://linkedin.com/in/amritacharya",
                "competitive_signal": "Significant focus on Defense and Aerospace supply chains signals higher-margin pivots",
                "hire_from": ["ITC", "Tata Steel", "McKinsey"]
            }
        ]
    },
    "Ninjacart": {
        "founded": 2015,
        "hq": "Bangalore",
        "founders": ["Thirukumaran Nagarajan"],
        "valuation_usd_bn": 0.8,
        "last_round": "Series D",
        "last_round_amount_usd_m": 145,
        "last_round_year": 2021,
        "total_raised_usd_m": 368,
        "investors": ["Tiger Global", "Walmart", "Flipkart"],
        "employee_count_approx": 3000,
        "revenue_model": "Wholesale margin on fresh produce",
        "primary_customers": "Retailers, Supermarkets, Kirana shops",
        "icp": "Urban grocery retailer needing daily fresh vegetable supply",
        "products": ["B2B Fresh Produce", "FMCG Wholesale", "Credit"],
        "known_gaps": [
            "High cash burn due to massive logistics wastage costs",
            "Farmer-side adoption still relies heavily on manual intervention",
            "Profitability elusive in core fresh produce B2B operations"
        ],
        "competitive_moat": "Deepest directly-connected farmer supply chain in India",
        "threat_from": ["WayCool", "DeHaat", "Udaan"],
        "twitter_handle": "Ninjacart",
        "reddit_search_term": "Ninjacart logistics problems",
        "leadership": [
            {
                "name": "Thirukumaran Nagarajan",
                "role": "CEO & Co-founder",
                "background": "IIM Kozhikode, ex-TaxiForSure",
                "known_for": "Pioneering the data-driven farm-to-retail model in India",
                "linkedin_url": "https://linkedin.com/in/thirunagarajan",
                "competitive_signal": "Focusing on 'Marketplace' rather than inventory-led model to reduce burn",
                "hire_from": ["Swiggy", "Walmart India", "WayCool"]
            }
        ]
    },
    "Locus": {
        "founded": 2015,
        "hq": "Bangalore",
        "founders": ["Nishith Rastogi", "Geet Garg"],
        "valuation_usd_bn": 0.3,
        "last_round": "Series C",
        "last_round_amount_usd_m": 50,
        "last_round_year": 2021,
        "total_raised_usd_m": 80,
        "investors": ["GIC", "Tiger Global", "Falcon Edge"],
        "employee_count_approx": 400,
        "revenue_model": "B2B Enterprise SaaS licensing",
        "primary_customers": "FMCG, E-commerce, 3PL",
        "icp": "Enterprise supply chain head looking to optimize last-mile routing",
        "products": ["Route Optimization", "Fleet Tracking", "Territory Planning"],
        "known_gaps": [
            "Implementation cycles for large enterprises take 6-12 months",
            "Global expansion proving difficult against entrenched legacy tools",
            "High churn in mid-market SME segment due to pricing"
        ],
        "competitive_moat": "Proprietary algorithmic routing IP contextualized for Asian road chaos",
        "threat_from": ["FarEye", "ClickPost", "Google Maps Mobility APIs"],
        "twitter_handle": "Locus_sh",
        "reddit_search_term": "Locus.sh routing software",
        "leadership": [
            {
                "name": "Nishith Rastogi",
                "role": "CEO & Founder",
                "background": "BITS Pilani, ex-Amazon ML",
                "known_for": "Expert in algorithmic logic for intra-city logistics",
                "linkedin_url": "https://linkedin.com/in/nishithrastogi",
                "competitive_signal": "Expanding into middle-mile optimization and global market entries (SE Asia, ME)",
                "hire_from": ["Amazon", "Oracle", "Rivigo"]
            }
        ]
    },
    "Porter": {
        "founded": 2014,
        "hq": "Bangalore",
        "founders": ["Pranav Goel", "Uttam Digga", "Vikas Choudhary"],
        "valuation_usd_bn": 0.5,
        "last_round": "Series E",
        "last_round_amount_usd_m": 100,
        "last_round_year": 2021,
        "total_raised_usd_m": 130,
        "investors": ["Peak XV", "Tiger Global", "Lightrock"],
        "employee_count_approx": 1500,
        "revenue_model": "Freight marketplace take-rate (commission per trip)",
        "primary_customers": "SMEs, FMCG distributors, D2C brands",
        "icp": "Urban SME needing ad-hoc mini-trucks for intra-city delivery",
        "products": ["Mini Trucks", "2-Wheeler Delivery", "Packers & Movers"],
        "known_gaps": [
            "Driver retention issues due to fluctuating incentives",
            "Intense price wars destroying unit economics",
            "Damage to goods during transit frequently reported by users"
        ],
        "competitive_moat": "Largest active mini-truck driver fleet density in Tier-1 cities",
        "threat_from": ["Borzo", "Blowhorn", "Ola/Uber Freight"],
        "twitter_handle": "Porter_India",
        "reddit_search_term": "Porter app drivers refusing",
        "leadership": [
            {
                "name": "Pranav Goel",
                "role": "CEO & Co-founder",
                "background": "IIT Kharagpur, ex-J.P. Morgan",
                "known_for": "Leading India's largest intra-city logistics marketplace",
                "linkedin_url": "https://linkedin.com/in/pranav-goel-b8384b1b",
                "competitive_signal": "Integrating EV fleets at scale to combat rising fuel costs and ESG requirements",
                "hire_from": ["ITC", "Ola", "Blowhorn"]
            }
        ]
    },
    "ElasticRun": {
        "founded": 2016,
        "hq": "Pune",
        "founders": ["Sandeep Deshmukh", "Saurabh Nigam", "Shitiz Bansal"],
        "valuation_usd_bn": 1.5,
        "last_round": "Series E",
        "last_round_amount_usd_m": 330,
        "last_round_year": 2022,
        "total_raised_usd_m": 430,
        "investors": ["SoftBank", "Kalaari", "Prosus Ventures"],
        "employee_count_approx": 2000,
        "revenue_model": "B2B rural e-commerce margins",
        "primary_customers": "FMCG Brands and Rural Kirana Stores",
        "icp": "FMCG major seeking distribution reach into deep rural villages",
        "products": ["Rural Distribution", "Credit for Kiranas", "E-commerce Logistics"],
        "known_gaps": [
            "Heavily reliant on FMCG majors (low margin profile)",
            "Operations are highly asset-heavy and logistically complex",
            "Slowdown in rural consumption directly slashes throughput"
        ],
        "competitive_moat": "Crowdsourced logistics network reaching 80,000+ deep rural villages",
        "threat_from": ["Udaan", "JioMart B2B", "Direct FMCG distributors"],
        "twitter_handle": "ElasticRun",
        "reddit_search_term": "Elasticrun rural logistics",
        "leadership": [
            {
                "name": "Sandeep Deshmukh",
                "role": "CEO & Co-founder",
                "background": "IIM Ahmedabad, ex-Amazon (Rural lead)",
                "known_for": "Built the 'Deep-Reach' logistics network for rural India",
                "linkedin_url": "https://linkedin.com/in/sandeep-deshmukh-0b8152",
                "competitive_signal": "Focusing on 'Credit for Kirana Stores' to improve order frequency and stickiness",
                "hire_from": ["Amazon", "Apple", "Marico"]
            }
        ]
    },

    # ---------------- Boutique Consulting ----------------
    "Redseer": {
        "founded": 2009,
        "hq": "Bangalore",
        "founders": ["Anil Kumar"],
        "valuation_usd_bn": None,
        "last_round": "Bootstrapped",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2023,
        "total_raised_usd_m": 0,
        "investors": [],
        "employee_count_approx": 350,
        "revenue_model": "Consulting retainers + bespoke reports",
        "primary_customers": "PE/VC firms, Startups plotting IPOs",
        "icp": "Late-stage startup founder needing a market-mapping report for DRHP",
        "products": ["Market Sizing", "Due Diligence", "IPO Advisory"],
        "known_gaps": [
            "Criticized for overly optimistic TAM projections for startups",
            "Struggle to compete in heavy operational transformation consulting",
            "Talent frequently poached by MBB firms"
        ],
        "competitive_moat": "Defacto standard for Indian startup/e-commerce market sizing reports",
        "threat_from": ["Bain & Co (Tech Practice)", "Praxis", "Big 4"],
        "twitter_handle": "RedSeer",
        "reddit_search_term": "Redseer consulting salary",
        "leadership": [
            {
                "name": "Anil Kumar",
                "role": "Founder & CEO",
                "background": "IIT Delhi, ex-Zinnov",
                "known_for": "Defining market sizing for the Indian internet economy",
                "linkedin_url": "https://linkedin.com/in/anil-kumar-redseer",
                "competitive_signal": "Expanding research into the 'Next Billion Users' segments to differentiate from generalist firms",
                "hire_from": ["Zinnov", "Kearney", "EY"]
            }
        ]
    },
    "Praxis": {
        "founded": 2018,
        "hq": "Delhi",
        "founders": ["Madhur Singhal"],
        "valuation_usd_bn": None,
        "last_round": "Bootstrapped",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2023,
        "total_raised_usd_m": 0,
        "investors": [],
        "employee_count_approx": 250,
        "revenue_model": "Consulting fees",
        "primary_customers": "PE funds, IT Services, Healthcare",
        "icp": "Private Equity partner needing commercial due diligence in 3 weeks",
        "products": ["Commercial Due Diligence", "Value Creation", "Growth Strategy"],
        "known_gaps": [
            "Lower brand recall vs Redseer in consumer-tech",
            "Heavy partner-driven sales dependency",
            "Burnout culture similar to MBB but with boutique pay"
        ],
        "competitive_moat": "Extremely fast turnaround on PE due diligence sprints",
        "threat_from": ["Redseer", "EY Parthenon", "Kearney"],
        "twitter_handle": "PraxisGA",
        "reddit_search_term": "Praxis global alliance work culture",
        "leadership": [
            {
                "name": "Madhur Singhal",
                "role": "Managing Partner & CEO",
                "background": "IIT Delhi, IIM Ahmedabad, ex-Bain",
                "known_for": "Expert in PE due diligence and value creation",
                "linkedin_url": "https://linkedin.com/in/madhurs",
                "competitive_signal": "Hiring data scientists to build a 'Tech-led' consulting vertical",
                "hire_from": ["Bain & Company", "Zinnov", "BCG"]
            }
        ]
    },
    "Alvarez & Marsal": {
        "founded": 1983,
        "hq": "New York / Mumbai",
        "founders": ["Tony Alvarez II", "Bryan Marsal"],
        "valuation_usd_bn": None,
        "last_round": "Private",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2024,
        "total_raised_usd_m": 0,
        "investors": [],
        "employee_count_approx": 8000,
        "revenue_model": "Turnaround and restructuring fees",
        "primary_customers": "Distressed assets, PEs, Boards",
        "icp": "Bankrupt/distressed enterprise board needing an interim CEO/CRO",
        "products": ["Turnaround Management", "Restructuring", "Disputes / Investigations"],
        "known_gaps": [
            "Extremely high billing rates alienate mid-market companies",
            "Viewed historically as 'the grim reaper' (liquidators)",
            "Aggressive internal up-or-out culture"
        ],
        "competitive_moat": "The undisputed global leader in corporate restructuring/turnarounds",
        "threat_from": ["FTI Consulting", "AlixPartners", "Big 4 Restructuring"],
        "twitter_handle": "alvarezmarsal",
        "reddit_search_term": "Alvarez Marsal consulting restructuring",
        "leadership": [
            {
                "name": "Vikram Utamsingh",
                "role": "Managing Director & Country Lead, India",
                "background": "Ex-KPMG Head of Transactions",
                "known_for": "Pioneering the corporate restructuring and turnaround practice in India",
                "linkedin_url": "https://linkedin.com/in/vikram-utamsingh",
                "competitive_signal": "Recent public statements on increasing distressed asset opportunities in the mid-market",
                "hire_from": ["KPMG", "PwC", "Deloitte"]
            }
        ]
    },
    "Kroll": {
        "founded": 1932,
        "hq": "New York / Mumbai",
        "founders": ["Jules Kroll (Duff & Phelps merged)"],
        "valuation_usd_bn": None,
        "last_round": "Private Equity",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2024,
        "total_raised_usd_m": 0,
        "investors": ["Stone Point Capital", "Further Global"],
        "employee_count_approx": 6500,
        "revenue_model": "Valuation modeling + Forensics consulting",
        "primary_customers": "Law firms, PEs, Startups",
        "icp": "Unicorn CFO requiring 409a valuations or forensic fraud investigation",
        "products": ["Valuation", "Forensic Investigations", "Cyber Risk"],
        "known_gaps": [
            "Highly specialized, making cross-selling strategy consulting hard",
            "Fragmented brand identity (Duff & Phelps rebrand confusion)",
            "Commoditization of basic valuation services by smaller CA firms"
        ],
        "competitive_moat": "Gold standard for legally defensible forensic investigations and M&A valuations",
        "threat_from": ["FTI Consulting", "Big 4 Forensics"],
        "twitter_handle": "KrollWire",
        "reddit_search_term": "Kroll valuation interview",
        "leadership": [
            {
                "name": "Tarun Bhatia",
                "role": "Managing Director & Head of South Asia",
                "background": "Ex-CRISIL",
                "known_for": "Leader in forensic investigations and risk advisory",
                "linkedin_url": "https://linkedin.com/in/tarun-bhatia",
                "competitive_signal": "Focusing on M&A valuation services for the tech ecosystem",
                "hire_from": ["CRISIL", "EY", "Grant Thornton"]
            }
        ]
    },
    "Analysys Mason": {
        "founded": 1985,
        "hq": "London / Delhi",
        "founders": ["Simon Mason"],
        "valuation_usd_bn": None,
        "last_round": "Private",
        "last_round_amount_usd_m": 0,
        "last_round_year": 2024,
        "total_raised_usd_m": 0,
        "investors": ["Bridgepoint"],
        "employee_count_approx": 400,
        "revenue_model": "TMT specialized consulting + Research subscriptions",
        "primary_customers": "Telecom operators, Regulators, Tech infra funds",
        "icp": "Telecom CEO planning 5G spectrum auction strategy and fiber rollout",
        "products": ["Strategy Consulting", "Telecom Research", "M&A Advisory"],
        "known_gaps": [
            "Micro-niche focus restricts them entirely to TMT (Telecom/Media/Tech)",
            "Struggle to win broad consumer/retail mandates",
            "Scale is small compared to generalist tier-2 firms"
        ],
        "competitive_moat": "Unmatched vertical depth in Telecom regulations and infra strategy",
        "threat_from": ["Arthur D. Little", "Oliver Wyman", "MBB TMT practices"],
        "twitter_handle": "AnalysysMason",
        "reddit_search_term": "Analysys mason telecom consulting",
        "leadership": [
            {
                "name": "Rohan Dhamija",
                "role": "Managing Partner, Middle East & India",
                "background": "IIM Ahmedabad",
                "known_for": "Specialist in TMT (Telecom, Media, Tech) strategy and spectrum auctions",
                "linkedin_url": "https://linkedin.com/in/rohandhamija",
                "competitive_signal": "Deeply involved in 5G rollout strategies for Indian telcos",
                "hire_from": ["Ericsson", "Nokia", "Arthur D. Little"]
            }
        ]
    }
}
