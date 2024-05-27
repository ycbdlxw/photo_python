import mysql.connector
import cv2
# import matplotlib.pyplot as plt
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
# 批量生成face脸部图片
def face_image(bboxes, i, filepath,target_path):
    result1 = os.path.split(filepath)
    file_name = os.path.splitext(result1[1])
    datas = []
    for i in range(len(bboxes)):
        bbox = bboxes[i].astype(np.int32)
        # file_path=os.path.join(im_path,'')
        im = cv2.imread(filepath)
        # [h,w]根据自己图片中目标的位置修改
        x1, y1, x2, y2 = bbox
        width= int(x2-x1)
        heigh = int(y2 -y1)
        if heigh > 80 and width > 100:
            im = im[y1:y2, x1:x2]
            save_path_file = os.path.join(target_path, file_name[0][:16] + '_' + 'face_' + str(i) + '.jpg')
            cv2.imwrite(save_path_file, im)
            if not os.path.exists(save_path_file):
                continue

            image_var = get_image_var(save_path_file)
            if image_var < 100:
                os.remove(save_path_file)
                continue
            file_stats = os.stat(save_path_file)
            i = i + 1
            list1 = [result1[1], i - 1, width, heigh, file_stats.st_size, image_var]
            tup = tuple(list1)
            datas.append(tup)
def show_image(image_file):
    img_draw = plt.imread(image_file)
    plt.imshow(img_draw)
    plt.axis('off')
    plt.show()


def save_image(filepath, image):
    result1 = os.path.split(filepath)
    file_name = os.path.splitext(result1[1])
    save_path = result1[0] + '/human/' + file_name[0] + ".jpg"
    cv2.imwrite(save_path, image)


def save_image_png(filepath, image):
    result1 = os.path.split(filepath)
    file_name = os.path.splitext(result1[1])
    save_path = result1[0] + "/" + file_name[0] + ".png"
    if not os.path.exists(save_path):
       cv2.imwrite(save_path, image)
    else :
        logging.info(f'{save_path} is exit')


def get_image_var(img_path):
    image = cv2.imread(img_path);
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_var = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return image_var


def get_save_file(img_path, insert_name, extent_name):
    return os.path.join(img_path, insert_name, extent_name)


# 递归输出当前路径下所有目录子文件
def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
            list_name.append(file_path)


# def get_file_name(mode, path):  #
#     file_path = ""
#     match mode:
#         case 2:
#             if 'person' in path:
#                 file_path = path
#             else:
#                 file_path = ""

#         case _:
#             file_path = path
#     return file_path


def init_mysql():
    mydb = mysql.connector.connect(
        host="home.ycbd.work",
        user="root",
        passwd="ycbd74mysql!@#",
        database="photo"
    )
    return mydb


def create_table(table, primary, colums):
    sql = f"CREATE TABLE {table} ({primary} int unsigned NOT NULL AUTO_INCREMENT COMMENT '表键ID', {colums}) ENGINE=InnoDB  DEFAULT " \
          f"CHARSET=utf8mb3 COMMENT='脸部信息' "
    try:
        mydb = init_mysql()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except Exception as e:
        print("error:", e, sql)


def count_values(body, number):
    count = 0
    for i in range(len(body)):
        if body[i] > number:
            count = count + 1
    return count


def is_valid(body, number):
    for i in range(len(body)):
        if body[0] < number:
            return False


def insert(table, columns, values):
    sql = f"insert into {table} ({columns}) VALUES ("
    # sql = f"insert into face_data ({columns}) VALUES ("
    i = 0
    colstr = str.split(columns, ",")
    n = len(colstr)
    while i <= n - 1:
        if i == 0:
            sql += "%s"
        else:
            sql += ",%s"
        i = i + 1
    sql += f")"
    try:
        mydb = init_mysql()
        mycursor = mydb.cursor()
        # 元组方式传参
        # print("sql: "+sql)
        mycursor.executemany(sql, values)
    except Exception as e:
        print("error:", e, sql)
        pass
    finally:
        mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    return mycursor.lastrowid


def query(table, colums, where):
    sql = f"SELECT {colums} FROM {table}   where {where}"
    try:
        mydb = init_mysql()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
    except Exception as e:
        print("error:", e, sql)
        pass
    finally:
        pass
    return myresult


def update(table, updates, where):
    sql = f"SELECT {updates} FROM {table}   where {where}"
    try:
        mydb = init_mysql()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
    except Exception as e:
        print("error:", e, sql)
        pass
    return mycursor.rowcount
