from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
pages_number = 199  # Reduced for testing
car_details = []

def Dubizzel():
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
            url = f'https://www.dubizzle.com.eg/en/vehicles/cars-for-sale/used/?page={n}&filter=price_between_0_to_5000000%2Cyear_between_2000_to_2026'  # Fixed: use n
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

            # Try different possible class names for car listings
            car_list = browser.find_elements('css selector', '[class*="_70cdfb32"], [class*="listing"], .listing-item, .search-result-item')
            
            if not car_list:
                print("No cars found on this page. The site might have changed structure.")
                # Try to get page content for debugging
                print("Page title:", browser.title)
                continue

            print(f"Found {len(car_list)} cars on page {n}")

            for car in car_list:
                try:
                    html_code = car.get_attribute('outerHTML')
                    soup = BeautifulSoup(html_code, 'html.parser')
                    
                    # More flexible selectors with multiple fallbacks
                    
                    try:
                        Car_Price = soup.find(['span', 'div'], class_=['ddc1b288', 'price', 'amount']).text.strip()
                    except:
                        Car_Price = 'Not Found'
                    
                    try:
                        Car_name = soup.find(['h2', 'h3'], class_=['_562a2db2', 'title', 'name']).text.strip()
                    except:
                        Car_name = 'Not Found'
                    
                    try:
                        Car_year = soup.find(['span', 'div'], class_=['_18b01e88', 'year', 'model-year']).text.strip()
                    except:
                        Car_year = 'No Car_year'
                    
                    try:
                        # Fixed: Use more generic selectors for mileage
                        Mileage = soup.find(['span', 'div'], class_=['mileage', 'km']).text.strip()
                    except:
                        Mileage = 'No Mileage'
                    
                    try:
                        FuelType = soup.find(['span', 'div'], class_=['_3e1113f0', 'fuel-type']).text.strip()
                    except:
                        FuelType = 'Not Found'
                    
                    try:
                        Location = soup.find(['span', 'div'], class_=['f7d5e47e', 'location', 'area']).text.strip()
                    except:
                        Location = 'Not Found'
                    
                    try:
                        Creation_date = soup.find(['span', 'div'], class_=['c72cec28', 'date', 'posted']).text.strip()
                    except:
                        Creation_date = 'No Creation date'
                    
                    try:
                        Contect_method = soup.find(['span', 'div'], class_=['_30de236c', 'contact', 'seller-type']).text.strip()
                    except:
                        Contect_method = 'Not Found'
                    
                    car_details.append({
                        'Car_Price': Car_Price,
                        'Car_name': Car_name,
                        'Mileage': Mileage,
                        'Car_year': Car_year,
                        'Location': Location,
                        'Creation_date': Creation_date,
                        'FuelType': FuelType,
                        'Contect_method': Contect_method,
                        'Page': n
                    })
                    
                except Exception as car_error:
                    print(f"Error processing a car: {car_error}")
                    continue
            
            print(f"Total cars collected so far: {len(car_details)}")
            
            # Add delay between pages
            if n < pages_number:
                time.sleep(1)

    except Exception as e:
        print(f'something went wrong with Dubizzel ==> {e}')
    finally:
        if 'browser' in locals():
            browser.close()

def Printing_file():
    try:
        if not car_details:
            print("No data to save!")
            return
            
        path = './Dubizzle_product.csv'
        columns = car_details[0].keys()
        with open(path, 'w', newline='', encoding='UTF-8') as output_file:
            dict_writer = csv.DictWriter(output_file, columns)
            dict_writer.writeheader()
            dict_writer.writerows(car_details)
        print(f'File Printed Successfully with {len(car_details)} records')
    except Exception as e:
        print(f'something went wrong with Printing_file ==> {e}')

# Run the functions
Dubizzel()
Printing_file()