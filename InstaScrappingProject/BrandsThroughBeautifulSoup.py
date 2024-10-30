import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import instaloader

# Setup Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the page
driver.get("https://starngage.com/plus/en-us/brand/ranking/instagram/pakistan/shopping")

# Wait for the specific element to be present
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "name.mb-1.fw-bold")))

# Parse page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract brand names
all_brands = []
for div in soup.find_all('div', class_='name mb-1 fw-bold'):
    link = div.find('a', class_='link color-pink text-break')
    if link:
        brand_name = link.text.strip()
        all_brands.append(brand_name)

# Clean up the driver
driver.quit()

# Process brand names: Remove the '@' symbol and ensure uniqueness
all_brands = [brand_name.replace('@', '') for brand_name in all_brands]

# Randomly select 30 brand names from the list
brands = random.sample(all_brands, min(30, len(all_brands)))

# Login to Instagram with Instaloader
L = instaloader.Instaloader()
L.login('your_username', 'your_password')  # Replace with your Instagram credentials

# Collect brand profile data
brand_data = []

def get_profile_info(brand_name):
    try:
        profile = instaloader.Profile.from_username(L.context, brand_name)
        return {
            "brand": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "bio": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "is_private": profile.is_private
        }
    except Exception as e:
        print(f"Error fetching profile for {brand_name}: {str(e)}")
        return None

for brand in brands:
    info = get_profile_info(brand)
    if info:
        brand_data.append(info)

# Convert the list of brands to a DataFrame
df = pd.DataFrame(brand_data)

# Save the DataFrame to an Excel file
output_file = "instagram_brands.xlsx"
df.to_excel(output_file, index=False)

print(f"Brand profile data saved to {output_file}")
