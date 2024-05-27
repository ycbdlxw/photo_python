import exifread
import pytz
from PIL import Image
from datetime import datetime
import logging
import os
import logging
def get_file_logger(logger_name, log_file_path):
    """
    配置文件日志输出并返回logger对象
    """
    # 创建logger对象并设置日志级别
    logger = logging.getLogger(logger_name)
    if logger_name=='error':
        logger.setLevel(logging.ERROR)
    else:
      logger.setLevel(logging.INFO)

    # 创建FileHandler对象并设置日志级别和格式
    file_handler = logging.FileHandler(log_file_path, mode='w')
    if logger_name=='error':
        file_handler.setLevel(logging.ERROR)
    else:
      file_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    # 将FileHandler对象添加到logger对象中
    logger.addHandler(file_handler)

    # 返回logger对象
    return logger  

def get_image_capture_time(image_file_path):
    """
    获取图像文件的拍摄时间、make和mode信息
    """
    dt_object = None
    make = None
    mode = None
    gps_data = None

    # 检查路径是否存在或是否可读
    if not os.path.exists(image_file_path) or not os.access(image_file_path, os.R_OK):
        logging.error(f"文件 {image_file_path} 不存在或不可读")
        return None, None, None

    try:
        with Image.open(image_file_path) as img:
            # 获取make和mode信息
            make = img.format_description.split(',')[0].strip()
            mode = img.mode

            # 使用exifread库获取exif数据
            tags = exifread.process_file(open(image_file_path, 'rb'), details=False)
            # 获取GPS数据
            if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags and 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
                gps_data=1
            else:
                gps_data=0
            if 'EXIF DateTimeOriginal' in tags:
                dt_original = tags['EXIF DateTimeOriginal'].values
                if dt_original:
                    # 处理时区问题
                    tz_local = pytz.timezone('Asia/Shanghai')
                    dt_object = datetime.strptime(dt_original, "%Y:%m:%d %H:%M:%S").replace(tzinfo=tz_local)

    except Exception as e:
        logging.error(f"读取文件 {image_file_path} 的拍摄时间出错：{e}")

    if not dt_object:
        mtime = os.path.getmtime(image_file_path)
        dt_object = datetime.fromtimestamp(mtime)

    return dt_object, make, mode,gps_data
def save_gps_data_to_image(image_file, gps_data):
    # 打开图片文件
    image = Image.open(image_file)

    # 获取图片的Exif数据
    exif_data = image._getexif()

    # 将GPS数据添加到Exif数据中
    exif_data[34853] = {}

    for key in gps_data.keys():
        tag_id = GPSTAGS.get(key, key)
        exif_data[34853][tag_id] = gps_data[key]

    # 保存修改后的Exif数据
    image.save(image_file, exif=exif_data)