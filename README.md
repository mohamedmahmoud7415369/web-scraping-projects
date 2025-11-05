<!-- Banner / Header -->
<div align="center">
  <img src="https://media.giphy.com/media/3o7aD6qfI3Yxk9Ft4M/giphy.gif" width="250" alt="Web Scraping Code"/>
</div>

# Hi 👋 I’m **Mohamed Mahmoud**  
*Data & Web-Scraping Enthusiast | Manufacturing Background | Python & Data Pipeline Practitioner*

[![Profile Views](https://komarev.com/ghpvc/?username=mohamedmahmoud7415369&style=flat-square&color=blue)](https://github.com/mohamedmahmoud7415369)

---

## 🧰 About Me  
With a foundation in manufacturing (insulation foam & building materials), I’ve harnessed analytical and process-driven thinking, and now pivoting into programming, data science and automation.  
My current focus: **web scraping**, data ingestion, cleaning & analysis pipelines.  
Based in Suez, Egypt.  

---

## 🛠️ Skills & Tools  
Here’s a visual snapshot of the technologies I work with:

<div align="left">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"    alt="Python"     width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg"    alt="Pandas"     width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/beautifulsoup/beautifulsoup-original.svg" alt="BeautifulSoup" width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scrapy/scrapy-original.svg"               alt="Scrapy"      width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg"               alt="SQLite"      width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg"        alt="MySQL"       width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg"                     alt="Git"         width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg"               alt="GitHub"      width="40" height="40"/>  
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg"               alt="Docker"      width="40" height="40"/>  
</div>

**Core strengths:**
- Web scraping & automation (Python, BeautifulSoup, Scrapy)  
- Data extraction → cleaning → storing workflows  
- Relational databases (SQLite, MySQL) for scraped data  
- Version control + collaboration (Git & GitHub)  
- Applying manufacturing domain understanding to data workflows  

---

## 📁 Projects Overview  
Here’s a curated view of the major folders/projects in this repository, what they solve and which tools they use:

| Folder / Project | Description | Key tools & highlights |
|------------------|-------------|-----------------------|
| **`ecommerce_scraper/`** | Scrapes multiple e-commerce websites, aggregates product names, prices, availability, stores in database. | Python + Requests, BeautifulSoup, SQLite/MySQL, data cleaning |
| **`job_listings_pipeline/`** | Extracts job postings (roles, companies, salaries) from job boards, loads into table, does simple analytics. | Scrapy, Pandas, MySQL, basic dashboard (e.g., Jupyter Notebook) |
| **`news_aggregator/`** | Collects news articles from several websites, normalizes content, stores as JSON/CSV for downstream use. | BeautifulSoup, Pandas, CSV/JSON export, date/time parsing |
| **`dashboard_visualization/`** | Takes scraped data from other projects, builds summary visuals: trends, top X lists, alerts. | Matplotlib/Seaborn/Plotly, Pandas, Jupyter Notebook |
| **`manufacturing_data_scrape/`** | Applying domain knowledge: scrape building-materials / insulation foam product sites to analyse pricing, suppliers. | Python + BeautifulSoup/Scrapy, MySQL, domain data insights |

*(Feel free to rename or update these with your exact project folder names and details.)*

---

## 🚀 How to Get This Repo & Start  
Here’s how **you** can clone, explore and use this repository:

```bash
# Clone the repo
git clone https://github.com/mohamedmahmoud7415369/web-scraping-projects.git

# Navigate into the directory
cd web-scraping-projects

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # on Linux/macOS
# .\venv\Scripts\activate    # on Windows

# Install dependencies (if a requirements file exists)
pip install -r requirements.txt

# Explore a project folder, e.g. `ecommerce_scraper/`
cd ecommerce_scraper
python run_scraper.py   # or follow docs in that folder

# View results: check the database / CSVs / Jupyter notebooks.

# (For visualization folder)
cd ../dashboard_visualization
jupyter notebook   # open the notebook to view charts
