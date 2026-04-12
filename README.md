

# 🌍 GeoSupply Rebound Oracle v4.0

**Self-Evolving • Grok-History-Correlated • Multi-Region + Macro • AWS Ready**

The ultimate live rebound scanner and autonomous trading intelligence system.  
Evolved from v2.2 with **true self-learning Bayesian weight evolution**, history correlation engine, multi-region coverage, macro/options layer, and production-grade risk controls.

Live demo-ready single-file Streamlit app built as an elite full-stack quant + self-improving AI systems architect.

---

## ✨ Key Features (v4.0)

- **True Autonomous Self-Learning** — Bayesian weight optimizer that evolves after every Grok analysis and backtest
- **History Correlation Engine** — Automatically matches current setups to past Grok theses (e.g. "Apr 2025 rebound analogue — 68% win rate")
- **Multi-Region Live Scanner** — US, Europe (VOD.L, BP.L, GLEN.L), Asia (9988.HK), ASX mining, and Crypto 24/7
- **Macro + Options Layer** — VIX regime, 10-year yield (^TNX), OPEX proximity, gamma/skew proxy, and interaction terms
- **Advanced Backtester** — 10,000-path Monte-Carlo with **0.3% trailing stop**, pre-market volume gate, and OPEX-aware exits
- **Grok High-Conviction Thesis Generator** — One-click AI thesis with profit opportunity % and mandatory exit window
- **Structured JSON Logging + Correlation IDs** — Full traceability across every Grok call and DB write
- **SQLite Self-Healing Database** — `geosupply.db`, `weights_history`, `grok_analyses`, and `saved_signals`
- **AWS Ready** — Streamlit secrets + optional S3 backup support (boto3)

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/JeffStone69/XAi.git
cd XAi2. Install dependencies
Bashpip install -r requirements.txt
3. Set up secrets (critical)
Create folder .streamlit/ and file .streamlit/secrets.toml:
toml[alpha_vantage]
key = "CXJGLOIMINTIXQLE"

[grok]
key = "xai-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
Never commit your secrets — .streamlit/secrets.toml is already in .gitignore
4. Run the app
Bashstreamlit run analyserV4.py

📁 Project Structure
textXAi/
├── analyserV4.py                 ← Main single-file app (v4.0)
├── geosupply.db                  ← Auto-created SQLite database
├── grok_responses.log            ← Structured JSON logs
├── geosupply_errors.log          ← Error logging
├── .streamlit/secrets.toml       ← Your API keys (gitignored)
├── requirements.txt
├── .gitignore
└── README.md

🧬 Self-Evolution & Learning Loop
Every time you:

Generate a Grok thesis, or
Run the advanced backtester,

the app automatically:

Correlates performance with Grok’s textual suggestions
Performs Bayesian-style weight update
Saves to weights_history table
Shows drift in the Self-Learning Evolution tab


🌐 Multi-Region + Macro Dashboard

Real-time rebound leaderboard across all regions
Live market status banner (Europe, Asia, US pre-market)
VIX, ^TNX, OPEX countdown, and gamma-flip proxies folded into every Rebound Score


📈 Deployment Options

PlatformStatusNotesLocal Streamlit✅ Readystreamlit run analyserV4.pyStreamlit Community Cloud✅ ReadyPaste secrets in app settingsAWS Lightsail / Beanstalk✅ ReadyUse AWS Secrets Manager + S3Hugging Face Spaces✅ ReadyWorks with secrets

⚠️ Disclaimer
This is for educational and research purposes only.
Not financial advice. Past performance is not indicative of future results.
Always do your own due diligence.

📜 Changelog
v4.0 (April 2026)

Full autonomous self-learning Bayesian loop
History Correlation Engine with analogue matching
Multi-region + macro/options layer
Advanced Monte-Carlo backtester with exact Grok risk rules
Structured logging + correlation IDs
AWS-ready S3 backup support

Previous versions: See commit history

🔑 License
Apache-2.0 (same as original repo)

Built with ❤️ as a self-improving AI systems architect
Questions or want v5.0 features? Open an issue or ping me on 𝕏.
