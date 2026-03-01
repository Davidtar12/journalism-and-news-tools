# journalism-and-news-tools

Media intelligence toolkit: Google Analytics 4 audience reports, GDELT news queries, Google News aggregation, PushEngage push notification automation.

## Scripts

| Script | Description |
|--------|-------------|
| `monthly-visitors.py` | Pulls monthly unique visitors from Google Analytics 4 and outputs an Excel report |
| `averagesecond.py` | Calculates average session duration per month from GA4 data |
| `non-bogota.py` | GA4 segment: users from outside Bogotá — useful for geographic audience analysis |
| `wk-minus35b.py` | GA4 demographic report: users under 35 years old |
| `wk-month-female.py` | GA4 gender breakdown by month |
| `pushengageimport.py` | Bulk import subscriber email list into PushEngage push notification service |
| `pushengageimport-onecontact.py` | Import a single contact into PushEngage with custom segments/tags |
| `wk-GDELT-news.py` | Query GDELT event database for news events by keyword, country, and date range |
| `wk-combined-ggl-news-search.py` | Multi-keyword Google News search with deduplication across sources |
| `wk-google-news-search.py` | Single-keyword Google News search scraper — outputs headlines and URLs |
| `wk-downl-first-image-multiple-links.py` | Download the lead/hero image from a list of article URLs |
| `wk-quoteextractor.py` | Extract direct quotes and attributions from article text for journalism fact-checking |

## Prerequisites

- Python 3.9+
- **GA4 scripts**: Google Analytics Data API enabled + service account JSON (stored outside repo)
- **PushEngage scripts**: PushEngage account API key
- **GDELT/News scripts**: No API key required — uses public endpoints

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in PUSHENGAGE_API_KEY, GA4_PROPERTY_ID
```

Place your GA4 service account JSON outside the repo and set the path in `.env`.

## Usage

```bash
# Monthly visitors report (outputs Excel)
python monthly-visitors.py --property YOUR_GA4_PROPERTY_ID

# Search GDELT for news events
python wk-GDELT-news.py --keyword "climate change" --country "CO" --days 30

# Google News search
python wk-google-news-search.py --query "python automation" --output results.csv

# Bulk PushEngage subscriber import
python pushengageimport.py --csv subscribers.csv
```

## Notes

- GA4 service account needs **Viewer** role on the Analytics property.
- GDELT queries are free and public — no rate limiting but responses can be large.

## Built with

Python · Google Analytics Data API · GDELT API · PushEngage API · BeautifulSoup  
AI-assisted development (Claude, GitHub Copilot) — architecture, requirements, QA validation and debugging by me.
