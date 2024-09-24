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
driver.get("https://starngage.com/plus/en-us/influencer/ranking/instagram/pakistan")

# Wait for the specific element to be present
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "link.color-pink.text-break")))

# Parse page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract usernames
all_usernames = []
for link in soup.find_all('a', class_='link color-pink text-break'):
    username = link.text.strip()
    all_usernames.append(username)

# Clean up the driver
driver.quit()

# Process usernames: Remove the '@' symbol and ensure uniqueness
all_usernames = [username.replace('@', '') for username in all_usernames]

# Randomly select 100 usernames from the list
usernames = random.sample(all_usernames, min(100, len(all_usernames)))

# Login to Instagram with Instaloader
L = instaloader.Instaloader()
L.login('your_username', 'your_password')  # Replace with your Instagram credentials

# Collect profile data
profile_data = []

def get_profile_info(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print('billi',profile,'\n')
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "bio": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "is_private": profile.is_private
        }
    except Exception as e:
        print(f"Error fetching profile for {username}: {str(e)}")
        return None

for username in usernames:
    info = get_profile_info(username)
    if info:
        profile_data.append(info)

# Convert the list of profiles to a DataFrame
df = pd.DataFrame(profile_data)

# Save the DataFrame to an Excel file
output_file = "instagram_profiles.xlsx"
df.to_excel(output_file, index=False)

print(f"Profile data saved to {output_file}")
