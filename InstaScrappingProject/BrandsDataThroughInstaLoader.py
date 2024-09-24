import instaloader
import json

# Initialize Instaloader
L = instaloader.Instaloader()

# Login to Instagram (Replace with your credentials)
L.login('dummyUsername', 'dummyPassword')

# List of Influencer Usernames
brand_usernames = [
    # Pakistani Brands
    "khaadi",
    "gulahmedfashion",
    "sapphirepakistan",
    "ethnicpk",
    "alkaramstudio",
    "jdotofficial",
    "beechtreekids",
    "ego.offical",
    "bonanzasatrangi",
    "limelight.pret",

    # Indian Brands
    "fabindiaofficial",
    "bibaindia",
    "forest_essentials",
    "raw_mango",
    "amrapalijewels",
    "good.earth",
    "tanirugs",
    "vayaindia",
    "zariin",
    "theayurvedaexperience",

    # American Brands
    "glossier",
    "everlane",
    "warbyparker",
    "patagonia",
    "allbirds",
    "thirdlove",
    "brooklinen",
    "away",
    "bombas",
    "reformation",

    # European Brands
    "ganni",  # Denmark
    "baandshoes",  # Spain
    "veja",  # France
    "mariemejewelry",  # UK
    "blundstone",  # Australia
    "tedbaker",  # UK
    "byredo",  # Sweden
    "nanushka",  # Hungary
    "loewe",  # Spain
    "frescobol_carioca"  # Portugal
]


# Function to get profile information including the number of posts
def get_profile_info(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,  # Number of posts
            "bio": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "is_private": profile.is_private
        }
    except Exception as e:
        print(f"Error fetching profile for {username}: {str(e)}")
        return None

# Fetching profile data
profile_data = []
for username in brand_usernames:
    info = get_profile_info(username)
    if info:
        print(info)
        profile_data.append(info)

# Save the fetched data to a text file in JS-like object format
with open('brands_data.txt', 'w') as file:
    file.write(json.dumps(profile_data, indent=4))

print("Data saved to brands_data.txt")
