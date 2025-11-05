from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pandas as pd
import seaborn
import matplotlib
import csv
import json
import random

#input('what is the category of products you want scrapping? : ')
pages_number = 1  # Reduced for testing
Company_details = []

def Tech_Behemoths():
    try:
        # Set up Chrome options to avoid detection
        chrome_options = Options()
        
        # Anti-detection settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to prevent detection
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        for n in range(1, pages_number + 1):  # Fixed: use n instead of pages_number
            url = f'https://techbehemoths.com/companies?page={n}'  # Fixed: use n
            print(f"Scraping page {n}: {url}")
            
            browser.get(url)
            browser.maximize_window()
            
            # Random delay to appear more human-like
            time.sleep(2)
            
            # Check if we got blocked
            page_title = browser.title
            if "error" in browser.current_url.lower() or "block" in page_title.lower():
                print("Website blocked the request. Stopping...")
                break

            
            Company_list = browser.find_elements(By.XPATH , "//div[@class='co-list__itm']")
            
            if not Company_list:
                print("No Companys found on this page. The site might have changed structure.")
                # Try to get page content for debugging
                print("Page title:", browser.title)
                continue

            print(f"Found {len(Company_list)} Companys on page {n}")

            for Company in Company_list:
                try:
                    html_code = Company.get_attribute('outerHTML')
                    soup = BeautifulSoup(html_code, 'html.parser')
                    
                    # More flexible selectors with multiple fallbacks
                    
                    try:
                        Com_Name = soup.find('p',{'class':'co-box__name'} ).text.strip()
                    except:
                        Com_Name = 'No name'
                    try:
                        Com_Description = soup.find('p',{'class':'co-box__descr'}).text()
                    except:
                        Com_Description = 'Not Found'
                    try:
                        Com_Size = soup.find('span', {'class','value'})
                    except:
                        Com_Size = 'Not Found'
                    try:
                        Hourly_Rate = soup.find('span',{'class':'cco-box__tltip-txt flex-centered absolute'}).text().strip()
                    except:
                        Hourly_Rate = 'Not Found'
                    try:
                        Services = soup.find('div', {'class':'txt'}).text().strip()
                    except:
                        Services = 'Not Found'
                    try:
                        Company_URl = soup.find('a').get('href')
                    except:
                        Company_URl = 'Not Found'

                    Company_details.append({
                        'Com_Name': Com_Name,
                        'Page': n,
                        'Com_Size':Com_Size,
                        'Hourly_Rate':Hourly_Rate,
                        'Services':Services,
                        'Com_Description':Com_Description,
                        'Company_URl':'https://techbehemoths.com' + Company_URl
                    })
                    
                except Exception as Company_error:
                    print(f"Error processing a Company: {Company_error}")
                    continue
            
            print(f"Total Companys collected so far: {len(Company_details)}")
            
            # Add delay between pages
            if n < pages_number:
                time.sleep(1)

    except Exception as e:
        print(f'something went wrong with Tech_Behemoths ==> {e}')
    finally:
        if 'browser' in locals():
            browser.close()


def Printing_file():
    try:
        if not Company_details:
            print("No data to save!")
            return
            
        path = './Tech_Behemoths_Companies.csv'
        columns = Company_details[0].keys()
        with open(path, 'w', newline='', encoding='UTF-8') as output_file:
            dict_writer = csv.DictWriter(output_file, columns)
            dict_writer.writeheader()
            dict_writer.writerows(Company_details)
        print(f'File Printed Successfully with {len(Company_details)} records')
    except Exception as e:
        print(f'something went wrong with Printing_file ==> {e}')

def Transformation():
    data = pd.DataFrame(Company_details)
    data.head()



# Run the functions
Tech_Behemoths()
Printing_file()
Transformation()