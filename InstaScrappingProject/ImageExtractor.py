import os

# Path to the directory containing the .jpg files
directory = r"C:\Users\usama\OneDrive\Desktop\Industry Watch\React Native"

# Change the current working directory to the target directory
os.chdir(directory)

# Initialize a counter for renaming
count = 1

# Iterate over all .jpg files in the directory
for filename in os.listdir(directory):
    # Generate the new name
    new_name = f"{count}.jpg"

    # Rename the file
    os.rename(filename, new_name)
    print(f'Renamed: "{filename}" to "{new_name}"')

    # Increment the counter
    count += 1

print("Renaming completed!")
