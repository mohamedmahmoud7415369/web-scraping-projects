from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import pandas as pd
import csv
import re
from urllib.parse import urljoin

pages_number = 1  # Reduced for testing
Company_details = []

def Tech_Behemoths():
    try:
        # Set up Chrome options to avoid detection
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to prevent detection
        try:
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
        except Exception:
            # some webdriver_manager / selenium combos may raise here; ignore if not available
            pass

        base = "https://techbehemoths.com"
        for n in range(1, pages_number + 1):
            url = f'{base}/companies?page={n}'
            print(f"Scraping page {n}: {url}")
            browser.get(url)
            browser.maximize_window()
            time.sleep(2 + (0.5 * (n % 3)))  # small random-ish delay

            # quick block check
            if "error" in browser.current_url.lower() or "blocked" in browser.title.lower():
                print("Website blocked the request. Stopping...")
                break

            # Find company 'blocks' by locating the 'View profile' links and taking their nearest container
            # This is more robust than relying on specific class names
            profile_links = browser.find_elements(By.XPATH, "//a[contains(normalize-space(.), 'View profile') and contains(@href, '/company/')]")
            if not profile_links:
                # fallback: try to find any /company/ links
                profile_links = browser.find_elements(By.XPATH, "//a[contains(@href, '/company/')]")

            company_blocks = []
            for a in profile_links:
                try:
                    # get closest ancestor div/section/article that contains the card text
                    ancestor = a.find_element(By.XPATH, "./ancestor::div[.//a[contains(@href, '/company/')]][1]")
                    company_blocks.append(ancestor)
                except Exception:
                    # if that fails, try two levels up
                    try:
                        ancestor = a.find_element(By.XPATH, "./ancestor::div[1]")
                        company_blocks.append(ancestor)
                    except Exception:
                        continue

            # deduplicate web elements (avoid duplicates if same block picked multiple times)
            # we compare by outerHTML attribute to detect duplicates
            seen_html = set()
            unique_blocks = []
            for blk in company_blocks:
                try:
                    html = blk.get_attribute('outerHTML')[:2000]  # truncated for speed
                except Exception:
                    html = None
                if html and html not in seen_html:
                    seen_html.add(html)
                    unique_blocks.append(blk)

            if not unique_blocks:
                print("No company blocks found - site layout may have changed.")
                print("Page title:", browser.title)
                continue

            print(f"Found {len(unique_blocks)} company blocks on page {n}")

            for blk in unique_blocks:
                try:
                    # Get company-level text and links
                    block_text = blk.text or ""
                    lines = [ln.strip() for ln in block_text.splitlines() if ln.strip()]
                    # Basic heuristics:
                    Com_Name = lines[0] if lines else "No name"
                    
                    # Company URL - find the /company/ link inside block
                    try:
                        company_link_el = blk.find_element(By.XPATH, ".//a[contains(@href, '/company/')]")
                        Company_URl = company_link_el.get_attribute('href')
                        # convert relative to absolute if necessary
                        Company_URl = urljoin(base, Company_URl)
                    except Exception:
                        Company_URl = 'Not Found'

                    # Location: look for a line containing a comma (city, country)
                    Company_Location = 'Not Found'
                    for ln in lines[1:5]:  # check the following few lines
                        if ',' in ln and len(ln) < 80:
                            Company_Location = ln
                            break
                        # some pages have "City" as a link followed by country in next token, fallback to single-word location
                        if re.search(r'^[A-Za-z\s\-]{2,30}$', ln) and len(ln.split()) <= 3 and 'Team size' not in ln and 'Hourly' not in ln:
                            Company_Location = ln
                            break

                    # Team size
                    Com_Size = 'Not Found'
                    for ln in lines:
                        if ln.lower().startswith('team size') or 'team size' in ln.lower():
                            # examples: "Team size 50-249" or "Team size 2-9"
                            m = re.search(r'([0-9]+[\-\+]?[0-9]*)', ln.replace(',', ''))
                            if m:
                                Com_Size = ln.split('Team size')[-1].strip() or m.group(0)
                            else:
                                Com_Size = ln
                            break

                    # Hourly rate
                    Hourly_Rate = 'Not Found'
                    for ln in lines:
                        if 'hourly rate' in ln.lower() or ln.lower().startswith('hourly rate'):
                            # keep the whole line, e.g. "Hourly Rate $$$$$ $30-70/h" or "Hourly Rate Not revealed"
                            Hourly_Rate = ln
                            break

                    # Services: find the "Services" heading and collect the following tokens until 'View profile' or empty
                    Services = 'Not Found'
                    if 'Services' in block_text:
                        # try to extract following words after "Services"
                        svc_match = re.search(r'Services[:\s]*\n?(.*?)(?:View profile|Inquire Company|Team size|Hourly Rate)', block_text, re.S | re.I)
                        if svc_match:
                            Services = svc_match.group(1).strip().replace('\n', ' | ')
                        else:
                            # fallback: find line that contains common service names or many tokens
                            svc_lines = [ln for ln in lines if len(ln.split()) <= 6 and ln.lower() not in ('team size', 'hourly rate')]
                            if svc_lines:
                                Services = svc_lines[-1]

                    # Description: usually a sentence-like line after the name and location
                    Com_Description = 'Not Found'
                    # pick the first reasonably long line that is not name/location/team/hourly/services
                    for ln in lines[1:6]:
                        if len(ln) > 30 and not any(k in ln.lower() for k in ['team size', 'hourly rate', 'services', 'view profile', 'inquire']):
                            Com_Description = ln
                            break

                    Company_details.append({
                        'Com_Name': Com_Name,
                        'Page': n,
                        'Company_URl': Company_URl if Company_URl else 'Not Found',
                        'Company_Location': Company_Location,
                        'Com_Description': Com_Description,
                        'Com_Size': Com_Size,
                        'Hourly_Rate': Hourly_Rate,
                        'Services': Services
                    })

                    # small debug print
                    if len(Company_details) <= 5:
                        print("DEBUG CARD:")
                        print("Name:", Com_Name)
                        print("URL:", Company_URl)
                        print("Location:", Company_Location)
                        print("Size:", Com_Size)
                        print("Hourly:", Hourly_Rate)
                        print("Services:", Services)
                        print("Description:", Com_Description)
                        print("----")
                except Exception as Company_error:
                    print(f"Error processing a Company block: {Company_error}")
                    continue

    except Exception as e:
        print(f'something went wrong with Tech_Behemoths ==> {e}')
    finally:
        try:
            if 'browser' in locals():
                browser.quit()
        except Exception:
            pass