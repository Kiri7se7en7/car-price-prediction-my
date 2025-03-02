from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

# Paths to Brave browser and WebDriver
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
driver_path = "C:/webdriver/chromedriver.exe"  # Make sure this matches your Brave browser's version

# Mimic a real browser with randomized user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# Configure Selenium WebDriver options
options = Options()
options.binary_location = brave_path
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")  # Suppress logs
options.add_argument(f"user-agent={random.choice(user_agents)}")

# Toggle headless mode (Set to True to run in background)
HEADLESS_MODE = True  
if HEADLESS_MODE:
    options.add_argument("--headless=new")  

# Start WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)  # Set explicit wait

# Base URL
base_url = "https://www.carlist.my/cars-for-sale/malaysia?page="
page = 1
MAX_PAGES = 50  # Set a page limit to prevent infinite scraping

# Function to safely extract text
def safe_find_text(element, selector):
    try:
        return element.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return "N/A"  # Default value if element is missing

try:
    # Open CSV file to store results
    with open("carlist_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Car Name", "Transmission", "Mileage", "Price", "Location"])  # Fix header mismatch

        while page <= MAX_PAGES:
            print(f"🔍 Scraping page {page}...")
            url = base_url + str(page)
            driver.get(url)

            # Wait for listings to appear instead of using time.sleep()
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".listing")))
            except:
                print("⚠️ No more cars found or website structure changed. Stopping.")
                break

            # Find all car listings
            cars = driver.find_elements(By.CSS_SELECTOR, ".listing")
            print(f"✅ Found {len(cars)} car listings on page {page}")

            if not cars:
                print("⚠️ No car listings found! Website structure may have changed.")
                break

            for car in cars:
                try:
                    print("🔍 Scraping a new car...")
                    name = safe_find_text(car, ".listing__title")
                    price = safe_find_text(car, ".listing__price")
                    mileage = safe_find_text(car, ".listing__specs div:first-child")
                    transmission = safe_find_text(car, ".listing__specs div:nth-child(2)")
                    location = safe_find_text(car, ".listing__specs div:nth-child(4)")

                    print(f"✅ Car: {name} | Transmission: {transmission} | Mileage: {mileage} | Price: {price} | Location: {location}")
                    writer.writerow([name, transmission, mileage, price, location])  # Save to CSV

                except Exception as e:
                    print(f"❌ Error extracting details: {e}")

            page += 1
            time.sleep(random.uniform(1, 3))  # Random delay before next page

finally:
    driver.quit()
    print("✅ Scraping completed! Data saved to 'carlist_data.csv'.")
