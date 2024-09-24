import pandas as pd

# Read the Excel file
df = pd.read_excel('instagram_brands.xlsx')

# Open a text file to write the output
with open('instagram_brands.txt', 'w', encoding='utf-8') as file:
    for index, row in df.iterrows():
        # Create a dictionary for each row
        user_data = {
            'brand': row['brand'],
            'full_name': row['full_name'],
            'followers': row['followers'],
            'following': row['following'],
            'bio': row['bio'],
            'profile_pic_url': row['profile_pic_url'],
            'external_url': row['external_url'],
            'is_private': row['is_private']
        }

        # Write the dictionary as a string to the text file
        file.write(str(user_data) + ',\n')

print("Data saved to output.txt successfully!")
