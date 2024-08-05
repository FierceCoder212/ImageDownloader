import os

import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from Helpers.GoogleDriveHelper import GoogleDriverHelper
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # Log to a file
                        logging.StreamHandler()  # Log to the console
                    ])
logger = logging.getLogger(__name__)

helper = GoogleDriverHelper("Ersatzteil Images")
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}


def download_and_upload_image(image):
    url = image["image_url"]
    file_name = image["file_name"]
    try:
        print(f"Getting response for image {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Uploading image {file_name}")
            helper.upload_file_from_content(response.content, file_name)
            print(f"Image uploaded {file_name}")
            return None  # No error
        else:
            raise Exception(f'Image downloading error : {response.status_code}, {response.text}')
    except Exception as e:
        logger.error(f'Error downloading image : {e}')
        print(f"Error downloading image {image}")
        return image  # Return the image with an error
    finally:
        os.remove(file_name)


# helper.save_prev_drive_files_on_folder()

with open("images.json", "r") as all_images_data:
    all_data = json.load(all_images_data)
with open("Uploaded Files.json", "r") as all_uploaded_images:
    all_uploaded_data = json.load(all_uploaded_images)

all_data = [data for data in all_data if data["file_name"] not in all_uploaded_data]
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
