import requests
import json
import os

from GoogleDriveHelper import GoogleDriverHelper

helper = GoogleDriverHelper("Scag Images")
folder_path = "All Images"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
list_error_images = []
with open("images.json", "r") as all_images_data:
    all_data = json.load(all_images_data)

for image in all_data[0:1]:
    try:
        response = requests.get(image["image_url"])
        helper.upload_file_from_content(response.content, image["file_name"])
        print(response)

    except Exception as e:
        list_error_images.append(image)
        print(e)
        print(f"Error downloading image {image}")

with open("ErrorImages.josn", "w") as filename:
    filename.write(json.dumps(list_error_images, indent=4))
