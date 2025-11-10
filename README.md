# GScrapper
## About this project
GScrapper is a Python web scraping tool designed to extract academic paper information from **Google Scholar**. It supports both search results and author profile pages, with automatic pagination to retrieve all available articles. The tool exports data to CSV format for easy analysis and meta-analysis research.

### Key Features
- ✅ **Google Scholar Search Results** - Scrape papers from search queries
- ✅ **Google Scholar Author Profiles** - Extract all publications from researcher profiles
- ✅ **Full Pagination Support** - Automatically fetches all available articles (up to 100 per page)
- ✅ **CSV Export** - Clean, structured data export with titles, links, and citations
- ✅ **Smart Rate Limiting** - Built-in delays to avoid server blocking
---

## System Requirements
* **Python 3.12+** (recommended)
* **Python packages:**
  - `requests`
  - `beautifulsoup4`
  - `pandas`
* **Operating System:** Windows, macOS, or Linux

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/TheCurryGuy/GScrapper.git
cd GScrapper
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install requests beautifulsoup4 pandas
```

---

## Usage

### Quick Start
1. Run the script:
   ```bash
   python gscrapper.py
   ```

2. When prompted, paste one of the following URL types:
   - **Google Scholar Search**: `https://scholar.google.com/scholar?q=your+search+terms`
   - **Google Scholar Profile**: `https://scholar.google.com/citations?user=USER_ID`

3. Wait for the scraping to complete

4. Find your results in the generated CSV file:
   - `scrapped_gscholar.csv` - for search results
   - `scrapped_gscholar_profile.csv` - for author profiles

### Example URLs

**Search Results:**
```
https://scholar.google.com/scholar?q=machine+learning
```

**Author Profile:**
```
https://scholar.google.com/citations?user=VUlo65MAAAAJ&hl=en&oi=ao
```

### Output Format
The CSV file contains three columns:
- **Title** - Paper title
- **Links** - URL to the paper or citation page
- **References** - Author names, journal, year, and other citation details

---

## Features in Detail

### 🔍 Google Scholar Search Results
- Extracts papers from search query results
- Handles multiple pages automatically
- Respects rate limiting to avoid CAPTCHA

### 👤 Google Scholar Author Profiles
- Retrieves **all publications** from an author's profile
- Supports pagination (up to 100 articles per request)
- Extracts complete citation information
- Shows real-time progress during scraping

### 📊 Data Export
- Clean CSV format compatible with Excel, Google Sheets, etc.
- UTF-8 encoding for international characters
- Indexed rows for easy reference

---

## Important Notes & Disclaimer

⚠️ **Rate Limiting:** The script includes random delays (1-6 seconds) between requests to avoid overwhelming Google Scholar's servers.

⚠️ **CAPTCHA Risk:** Excessive scraping may trigger Google Scholar's CAPTCHA protection. If this happens:
- Wait a few hours before trying again
- Consider using a different network
- Reduce the frequency of requests

⚠️ **Responsible Use:** 
- Use this tool for academic and research purposes only
- Respect Google Scholar's terms of service
- Do not abuse the scraping functionality

⚠️ **Data Accuracy:** While the tool aims for accuracy, always verify critical information from original sources.

---

## Troubleshooting

### Error: "ReCaptcha is probably preventing the code from running"
**Solution:** Google Scholar has detected automated activity. Wait several hours and try again, or access the page in a browser first to solve any CAPTCHA.

### Error: "No articles found"
**Solution:** 
- Verify the URL is correct
- Check if the profile/search page loads in a browser
- Ensure you have an active internet connection

### Missing Dependencies
**Solution:** Install all required packages:
```bash
pip install requests beautifulsoup4 pandas
```

---

## Contributing
Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Submit pull requests with improvements
- Suggest new features

---

## License
See LICENSE file for details.

---

## Contact
Original Author: @thecurryguy
Twitter: https://github.com/thecurryguy

Modified version with enhanced Google Scholar profile support and full pagination.

---

**Star ⭐ this repository if you find it useful!**
