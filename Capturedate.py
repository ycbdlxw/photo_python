import mysql.connector
from mysql.connector import Error
from datetime import datetime
try:
    connection = mysql.connector.connect(user='root', password='Ycbd74mysql!@#',
                              host='home.ycbd.work', database='file')
    if connection.is_connected():
        print('Connected to MySQL database')
         # Parse file_name column and update Capturedate column
        update_query = '''
            UPDATE img_info_data
            SET Capturedate = %s
            WHERE file_name IS NOT NULL and id=%s
        '''
        with connection.cursor() as cursor:
            select_query = '''
                SELECT id,file_name
                FROM img_info_data where file_name REGEXP '^[0-9]{8}-[0-9]{6}$'
            '''
            cursor.execute(select_query)
            results = cursor.fetchall()
            for row in results:
                id = row[0]
                try:
                    # Try to parse file_name as a datetime object
                    capture_date = datetime.strptime(row[1], '%Y%m%d-%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                    values = (capture_date, id)
                    cursor.execute(update_query,values)
                    connection.commit()
                    print('Capturedate updated successfully')
                except ValueError:
                    # If file_name is not in a normal date format, set Capturedate to NULL
                    capture_date = None
                
            
            print('Capturedate updated successfully')
except Error as e:
    print('Error while connecting to MySQL', e)
finally:
    if connection.is_connected():
        connection.close()
        print('MySQL connection closed')