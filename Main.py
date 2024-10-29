import base64
import logging

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
    image_data = base64.b64decode(base_64_img)
    file_name = f'{section_diagram}.png'
    google_drive_helper.upload_file_from_content(file_bytes=image_data, file_name=file_name)
    print(f'Uploaded {file_name} to Google Drive.')
