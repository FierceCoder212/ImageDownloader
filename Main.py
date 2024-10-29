import base64
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Helpers.SqlLiteHelper import SQLiteHelper

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

google_drive_helper = GoogleDriverHelper('John Dheere Images')
db_file = r'C:\Workspace\JohnDeereScraper\Images.db'
sql_lite_helper = SQLiteHelper(db_file)

for section_diagram, base_64_img in sql_lite_helper.yield_fetch_all_records():
    try:
        base_64_img = base_64_img.replace('data:image/PNG;base64,', '')
        image_data = base64.b64decode(base_64_img)

        google_drive_helper.upload_file_from_content(file_bytes=image_data, file_name=section_diagram)
        print(f'Uploaded {section_diagram} to Google Drive.')

        if os.path.exists(section_diagram):
            os.remove(section_diagram)
    except Exception as ex:
        logger.error(f"Error processing {section_diagram}: {ex}")

print("All records have been uploaded to Google Drive.")
