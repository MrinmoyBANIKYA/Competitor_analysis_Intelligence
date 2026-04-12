# data/sector_meta.py

SECTOR_META = {
    "Fintech Payments": {
        "tam_usd_bn": 111.0,
        "sam_usd_bn": 12.5,
        "cagr_pct": 18.5,
        "saturation": "High",
        "saturation_score": 78,
        "market_stage": "Growth",
        "key_tailwinds": [
            "UPI transaction volume crossing 10Bn/month",
            "RBI push for credit at lower ticket sizes via digital lending",
            "ONDC disrupting B2B payments and commission structures"
        ],
        "unsolved_problems": [
            "Credit underwriting for thin-file users (no CIBIL history)",
            "Merchant MDR economics broken below Rs 500 transactions",
            "Cross-border payments still 3-5 day settlement latency"
        ],
        "reddit_pain_points": [
          "r/IndiaInvestments: 'Simpl keeps declining transactions without explanation'",
          "r/india: 'PhonePe UX getting worse with every update'",
          "r/startups: 'Razorpay support is nonexistent for small merchants'"
        ],
        "sector_risks": [
            "NPCI regulatory intervention on UPI market share caps",
            "Global fintech winter reducing VC appetite for cash burn",
            "Rising fraud rates (UPI fraud up 45% YoY)"
        ],
        "radar": {
            "saturation": 85,
            "capital_intensity": 70,
            "talent_scarcity": 60,
            "regulatory_risk": 90,
            "consumer_demand": 95,
            "white_space": 25
        },
        "radar_insight": "Highly regulated hyper-growth sector. Dominance defined by distribution and compliance resilience.",
        "players": {
            "public_companies": [
                {"name": "Paytm", "market_cap_usd_bn": 3.8, "stage": "Public", "hq": "Noida"}
            ],
            "private_giants": [
                {"name": "PhonePe", "valuation_usd_bn": 12.0, "stage": "Series E+", "hq": "Bangalore"},
                {"name": "Razorpay", "valuation_usd_bn": 7.5, "stage": "Series F", "hq": "Bangalore"}
            ],
            "rising_startups": [
                {"name": "Juspay", "valuation_usd_bn": 0.46, "stage": "Series C", "hq": "Bangalore"},
                {"name": "Simpl", "valuation_usd_bn": 0.24, "stage": "Series C", "hq": "Bangalore"}
            ]
        }
    },
    "Analytics Consulting": {
        "tam_usd_bn": 21.2,
        "sam_usd_bn": 3.5,
        "cagr_pct": 31.2,
        "saturation": "Medium",
        "saturation_score": 45,
        "market_stage": "Hypergrowth",
        "key_tailwinds": [
            "GenAI boom driving enterprise demand for custom LLMs",
            "Cloud migration 2.0: moving from storage to compute/AI",
            "Data-driven decision making becoming a board-level mandate"
        ],
        "unsolved_problems": [
            "Data silos in legacy Fortune 500 enterprises",
            "Translating raw data insights into measurable business ROI",
            "Talent shortage: finding 'bilingual' (tech + business) experts"
        ],
        "reddit_pain_points": [
            "r/startups: 'Analytics firms are becoming report factories, not strategic partners'",
            "r/india: 'Clients have incredibly messy data but expect magic results in a week'",
            "r/consulting: 'Insights are often stale by the time delivery cycle completes'"
        ],
        "sector_risks": [
            "In-housing of data teams by major tech giants",
            "Commoditization of basic BI and reporting services",
            "IP and security risks in handling sensitive enterprise data"
        ],
        "radar": {
            "saturation": 40,
            "capital_intensity": 30,
            "talent_scarcity": 95,
            "regulatory_risk": 40,
            "consumer_demand": 85,
            "white_space": 70
        },
        "radar_insight": "Talent-constrained market with massive white space in specialized LLM/MLOps consulting.",
        "players": {
            "public_companies": [
                {"name": "LatentView", "market_cap_usd_bn": 0.9, "stage": "Public", "hq": "Chennai"}
            ],
            "private_giants": [
                {"name": "Fractal", "valuation_usd_bn": 1.0, "stage": "Unicorn", "hq": "Mumbai"},
                {"name": "Tiger Analytics", "valuation_usd_bn": 0.6, "stage": "PE Backed", "hq": "Chennai"}
            ],
            "rising_startups": [
                {"name": "MathCo", "valuation_usd_bn": 0.35, "stage": "Series B", "hq": "Bangalore"},
                {"name": "Sigmoid", "valuation_usd_bn": 0.15, "stage": "Series B", "hq": "Bangalore"}
            ]
        }
    },
    "Wealthtech": {
        "tam_usd_bn": 8.6,
        "sam_usd_bn": 1.2,
        "cagr_pct": 18.8,
        "saturation": "Low-Medium",
        "saturation_score": 35,
        "market_stage": "Growth",
        "key_tailwinds": [
            "Financialization of Indian household savings into equity",
            "Smartphone penetration enabling Tier-2/3 retail participation",
            "Rise of robo-advisory and automated goal-based investing"
        ],
        "unsolved_problems": [
            "Transactional black holes: lag in visible app status vs fund movement",
            "High CAC for mass-market retail platforms",
            "Complex regulatory compliance with evolving SEBI norms"
        ],
        "reddit_pain_points": [
            "r/IndiaInvestments: 'INDmoney fee transparency is getting worse every day'",
            "r/investing_india: 'Zerodha outages during market volatility are unacceptable'",
            "r/india: 'Support for simple transaction errors takes 48+ hours'"
        ],
        "sector_risks": [
            "SEBI crackdown on finfluencer-driven user acquisition",
            "Market volatility leading to massive retail churn",
            "Potential cuts in distributor/broker commission caps"
        ],
        "radar": {
            "saturation": 55,
            "capital_intensity": 60,
            "talent_scarcity": 50,
            "regulatory_risk": 85,
            "consumer_demand": 90,
            "white_space": 45
        },
        "radar_insight": "Highly sensitive to regulatory shifts and market cycles. Success driven by trust and UX.",
        "players": {
            "public_companies": [
                {"name": "Angel One", "market_cap_usd_bn": 2.4, "stage": "Public", "hq": "Mumbai"}
            ],
            "private_giants": [
                {"name": "Zerodha", "valuation_usd_bn": 3.6, "stage": "Bootstrapped", "hq": "Bangalore"},
                {"name": "Groww", "valuation_usd_bn": 3.0, "stage": "Series E", "hq": "Bangalore"}
            ],
            "rising_startups": [
                {"name": "INDmoney", "valuation_usd_bn": 0.5, "stage": "Series D", "hq": "Gurugram"},
                {"name": "Smallcase", "valuation_usd_bn": 0.2, "stage": "Series C", "hq": "Bangalore"}
            ]
        }
    },
    "Supply Chain Tech": {
        "tam_usd_bn": 2.4,
        "sam_usd_bn": 0.8,
        "cagr_pct": 16.0,
        "saturation": "Low",
        "saturation_score": 22,
        "market_stage": "Early Growth",
        "key_tailwinds": [
            "National Logistics Policy driving unified tech standards",
            "D2C brand explosion requiring agile warehouse/delivery tech",
            "Shift to multi-modal connectivity (Rail+Road+Sea)"
        ],
        "unsolved_problems": [
            "Lack of real-time end-to-end visibility in deep logistics",
            "Fragmented communication between shippers and trackers",
            "Inability to integrate diverse data sources (IoT, GPS, ERP)"
        ],
        "reddit_pain_points": [
            "r/startups: 'Logistics tracking is still 50% manual spreadsheets and calls'",
            "r/india: 'Shipment delays are often hidden behind vague status updates'",
            "r/supplychain: 'Integration with legacy manufacturing ERPs is a nightmare'"
        ],
        "sector_risks": [
            "Fuel price volatility affecting unit economics",
            "High infrastructure dependency beyond pure software",
            "Driver and talent retention in the logistics layer"
        ],
        "radar": {
            "saturation": 30,
            "capital_intensity": 80,
            "talent_scarcity": 60,
            "regulatory_risk": 30,
            "consumer_demand": 75,
            "white_space": 85
        },
        "radar_insight": "Asset-heavy but digitally starved. High integration complexity creates deep defensibility.",
        "players": {
            "public_companies": [
                {"name": "Delhivery", "market_cap_usd_bn": 3.2, "stage": "Public", "hq": "Gurugram"}
            ],
            "private_giants": [
                {"name": "Zetwerk", "valuation_usd_bn": 2.8, "stage": "Series F", "hq": "Bangalore"},
                {"name": "ElasticRun", "valuation_usd_bn": 1.5, "stage": "Series E", "hq": "Pune"}
            ],
            "rising_startups": [
                {"name": "Locus", "valuation_usd_bn": 0.3, "stage": "Series C", "hq": "Bangalore"},
                {"name": "Porter", "valuation_usd_bn": 0.5, "stage": "Series E", "hq": "Bangalore"}
            ]
        }
    },
    "Boutique Consulting": {
        "tam_usd_bn": 8.2,
        "sam_usd_bn": 1.1,
        "cagr_pct": 12.7,
        "saturation": "Medium",
        "saturation_score": 52,
        "market_stage": "Mature",
        "key_tailwinds": [
            "SME digital transformation requiring high-touch advisory",
            "Need for specialized local expertise over generic Big 4 models",
            "Focus on cost-efficiency and direct ROI over brand prestige"
        ],
        "unsolved_problems": [
            "Value-based pricing misalignment with hourly billing defaults",
            "Lack of end-to-end implementation support post-advisory",
            "Scaling quality without diluting the senior partner touch"
        ],
        "reddit_pain_points": [
            "r/india: 'Fees are for reports that go into a bin, not for actual growth'",
            "r/consulting: 'Boutique pay with MBB work hours is a recipe for burnout'",
            "r/startups: 'Implementation setup takes months before any ROI is seen'"
        ],
        "sector_risks": [
            "Partner attrition: when a key leader leaves, the client follows",
            "Economic downturns slashing discretionary consulting spend",
            "Generative AI replacing entry-level research and analysis tasks"
        ],
        "radar": {
            "saturation": 65,
            "capital_intensity": 20,
            "talent_scarcity": 85,
            "regulatory_risk": 20,
            "consumer_demand": 60,
            "white_space": 40
        },
        "radar_insight": "Relationship-driven market undergoing a shift towards performance-linked mandates.",
        "players": {
            "public_companies": [],
            "private_giants": [
                {"name": "Alvarez & Marsal", "valuation_usd_bn": None, "stage": "Private", "hq": "New York/Mumbai"},
                {"name": "Kroll", "valuation_usd_bn": None, "stage": "PE Backed", "hq": "New York/Mumbai"}
            ],
            "rising_startups": [
                {"name": "Redseer", "valuation_usd_bn": None, "stage": "Bootstrapped", "hq": "Bangalore"},
                {"name": "Praxis", "valuation_usd_bn": None, "stage": "Partner Led", "hq": "Delhi"}
            ]
        }
    }
}
