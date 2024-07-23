import requests
import json
import os

folder_path="All Images"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open("images.json", "r") as all_images_data:
    all_data = json.load(all_images_data)

for image in all_data[0:5]:
    try:
        response = requests.get(image["image_url"])
        with open(f"All Images/{image["file_name"]}", "wb") as binaryimage:
            binaryimage.write(response.content)
        print(response)
        
    except Exception as e:
        print(f"Error downloading image {image}")
