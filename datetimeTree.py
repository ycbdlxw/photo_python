import mysql.connector
from datetime import datetime
 # Connect to the MySQL database
cnx = mysql.connector.connect(user='root', password='Ycbd74mysql!@#',
                              host='home.ycbd.work', database='file')
 # Get a cursor object
cursor = cnx.cursor()
 # Create the dateTimeTree table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS dateTimeTree (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关键ID',
  parentID INT NOT NULL COMMENT '父ID',
  level INT NOT NULL COMMENT '层级',
  name VARCHAR(255) NOT NULL COMMENT '名称'
)
"""
cursor.execute(create_table_query)
 # Select the file_name column from the img_info_data table
query = 'SELECT file_name FROM img_info_data'
cursor.execute(query)
rows = cursor.fetchall()
 # Loop through the rows and insert new directories into the dateTimeTree table
for row in rows:
    # Get the file_name value
    file_name = row[0]
     # Convert the file_name to a date-time format  
    try: 
        date_time_str = file_name.split('-')[0] 
        date_time_obj = datetime.strptime(date_time_str, '%Y%m%d') 
    except ValueError as e: 
        print("Error: ", e) 
        continue  # continue with next iteration of the loop
     # Insert the date-time values into the dateTimeTree table
    parent_id = -1
    for i, name in enumerate(['日期时间', str(date_time_obj.year), str(date_time_obj.month).zfill(2), str(date_time_obj.day).zfill(2)]):
        level = i
         # Check if the directory already exists in the dateTimeTree table
        query = 'SELECT id FROM dateTimeTree WHERE parentID=%s AND level=%s AND name=%s'
        values = (parent_id, level, name)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:
            # Insert the new directory into the dateTimeTree table
            insert_query = 'INSERT INTO dateTimeTree (parentID, level, name) VALUES (%s, %s, %s)'
            values = (parent_id, level, name)
            cursor.execute(insert_query, values)
            cnx.commit()
            parent_id = cursor.lastrowid
        else:
            # Update the parent ID for the next level
            parent_id = result[0]
     # Insert the file_name value into the dateTimeTree table
    insert_query = 'INSERT INTO dateTimeTree (parentID, level, name) VALUES (%s, %s, %s)'
    values = (parent_id, len(['日期时间', str(date_time_obj.year), str(date_time_obj.month).zfill(2), str(date_time_obj.day).zfill(2)]), file_name)
    # cursor.execute(insert_query, values)
 # Commit the changes
# cnx.commit()
 # Close the connection
cursor.close()
cnx.close()