import os
import imghdr
from PIL import Image
from exifread import process_file
from shutil import copyfile
from ImageTools import get_image_capture_time

output_dir_base = 'D:\\work\\myphotos'
input_dir ="C:\\Users\\ycbd\\Pictures" # "\\\\192.168.8.170\\相片\\photo\\2005"

image_list = []

def recursive_scan_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if imghdr.what(file_path) is not None:
                try:
                    # 打开文件并传递文件对象给process_file
                    with open(file_path, 'rb') as f:
                        exif = process_file(f)
                        brand, model = get_brand_model(exif)
                        creation_date = get_creation_date(exif)

                        output_dir = os.path.join(output_dir_base, f'{brand}\\{model}')
                        os.makedirs(output_dir, exist_ok=True)

                        copyfile(file_path, os.path.join(output_dir, filename))
                        image_list.append((filename, brand, model, creation_date))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        elif os.path.isdir(file_path):
            recursive_scan_dir(file_path)

recursive_scan_dir(input_dir)

for filename, brand, model, creation_date in image_list:
    print(f'{filename} ({brand} {model}) - {creation_date}')
