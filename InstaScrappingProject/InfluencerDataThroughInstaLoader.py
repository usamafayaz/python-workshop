import instaloader
import json

# Initialize Instaloader
L = instaloader.Instaloader()

# Login to Instagram (Replace with your credentials)
# L.login('dummyUsername', 'dummyPassword')

# List of Influencer Usernames
influencer_usernames = [
    # Pakistani Influencers
    "zaidalit",
    "dananeerr",
    "danyalzee",
    "amnayouzasaif",
    "usamatanveer010",
    "waseembadami_official",
    "sabaqamarzaman",
    "iamharis63",
    "mominamustehsan",
    "jawerya.ar",
    "asimazhar",
    "eyeina.shahzad",
    "iamkashee",
    "fizamuneeb1",
    "hamzaibrahimmm",
    "meer.oba",
    "_zain_zeta_",
    "la1ba.e",
    "glamupwitharfa",
    "aneeshaaly_",
    "hasnain._.solangi",
    "thisisjj47",
    "essaawww",
    "aunalikhosa",
    "_faiza77",

    # Indian Influencers
    "bhuvan.bam22",
    "kushakapila",
    "mostlysane",
    "ashishchanchlani",
    "amit_bhadana",
    "komalpandeyofficial",
    "dollysingh",
    "thatthinggirl",
    "siddharth93batra",
    "diipakhosla",
    "jasminxie3",
    "vamakshimagotra",
    "yashica.aa",
    "nishika_mehta1",
    "_riteeka7",
    "sheetal_599",
    "sonambajwa",

    # American Influencers
    "charlidamelio",
    "addisonraee",
    "zachking",
    "jamescharles",
    "hudabeauty",
    "chiaraferragni",
    "camerondallas",
    "lelepons",
    "nashgrier",
    "kayla_itsines",
    "mrbeast",
    "kimkardashian",
    "kyliejenner",
    "loganpaul",
    "jakepaul",
    "theellenshow",
    "shawnmendes",
    "arianagrande",
    "selenagomez",
    "dwaynejohnson",
    "ishowspeed",
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
for username in influencer_usernames:
    info = get_profile_info(username)
    if info:
        print(info)
        profile_data.append(info)

# Save the fetched data to a text file in JS-like object format
with open('influencer_data.txt', 'w') as file:
    file.write(json.dumps(profile_data, indent=4))

print("Data saved to influencer_data.txt")
