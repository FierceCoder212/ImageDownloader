import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from GoogleDriveHelper import GoogleDriverHelper

helper = GoogleDriverHelper("Scag Images")


def download_and_upload_image(image):
    try:
        url = image["image_url"]
        file_name = image["file_name"]
        print(f"Getting response for image {url}")
        response = requests.get(url)
        print(f"Uploading image {file_name}")
        helper.upload_file_from_content(response.content, file_name)
        print(f"Image uploaded {file_name}")
        return None  # No error
    except Exception as e:
        print(e)
        print(f"Error downloading image {image}")
        return image  # Return the image with an error


with open("images.json", "r") as all_images_data:
    all_data = json.load(all_images_data)
with open("Uploaded Files.json", "r") as all_uploaded_images:
    all_uploaded_data = json.load(all_uploaded_images)


all_data = [data for data in all_data if data["file_name"] not in all_uploaded_data]
print(all_data)
list_error_images = []

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(download_and_upload_image, image) for image in all_data]

    # Process the results as they complete
    for future in as_completed(futures):
        if error_image := future.result():
            list_error_images.append(error_image)

# Save the error images to a file
with open("ErrorImages.json", "w") as filename:
    filename.write(json.dumps(list_error_images, indent=4))
