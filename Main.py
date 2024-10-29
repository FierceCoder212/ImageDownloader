import base64
import logging
import os

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Helpers.SqlLiteHelper import SQLiteHelper

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # Log to a file
                        logging.StreamHandler()  # Log to the console
                    ])
logger = logging.getLogger(__name__)

google_drive_helper = GoogleDriverHelper('John Dheere Images')
sql_lite_helper = SQLiteHelper('Images.db')

# helper.save_prev_drive_files_on_folder()
for section_diagram, base_64_img in sql_lite_helper.yield_fetch_all_records():
    base_64_img = base_64_img.replace('data:image/PNG;base64,', '')
    image_data = base64.b64decode(base_64_img)
    google_drive_helper.upload_file_from_content(file_bytes=image_data, file_name=section_diagram)
    print(f'Uploaded {section_diagram} to Google Drive.')
    os.remove(section_diagram)
