import mysql.connector
 # Connect to the MySQL database
cnx = mysql.connector.connect(user='root', password='Ycbd74mysql!@#',
                              host='home.ycbd.work', database='file')
 # Get a cursor object
cursor = cnx.cursor()
 # Create the dirTree table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS dirTree (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关键ID',
  parentID INT NOT NULL COMMENT '父ID',
  level INT NOT NULL COMMENT '层级',
  name VARCHAR(255) NOT NULL COMMENT '名称'
)
"""
cursor.execute(create_table_query)
 # Select the directory column from the dirTree table
query = 'SELECT id, name FROM dirTree'
cursor.execute(query)
rows = cursor.fetchall()
 # Create a dictionary of existing directories
existing_directories = {row[1]: row[0] for row in rows}
 # Select the file_full column from the img_info_data table
query = 'SELECT file_full FROM img_info_data'
cursor.execute(query)
rows = cursor.fetchall()
 # Loop through the rows and insert new directories into the dirTree table
for row in rows:
    # Get the directory value
    file_full = row[0]
    
    if '/' in file_full:
        directory = file_full.split('/')[:-1]
    elif '\\' in file_full:
        directory = file_full.split('\\')[:-1]
    elif '_' in file_full:
        directory = file_full.split('_')
     # Loop through the directory levels and insert new rows into the dirTree table
    parent_id = 0
    index = -1;
    for i in range(len(directory)):
        level = i
        name = directory[i]
        index = index +1
        print(f'{file_full} , {name} 完成,{index}')
         # Check if the directory already exists in the dirTree table
        if name not in existing_directories:
            # Insert the new directory into the dirTree table
            insert_query = 'INSERT INTO dirTree (parentID, level, name) VALUES (%s, %s, %s)'
            values = (parent_id, level, name)
            cursor.execute(insert_query, values)
            existing_directories[name] = cursor.lastrowid
         # Update the parent ID for the next level
        parent_id = existing_directories[name]
 # Commit the changes
cnx.commit()
 # Close the connection
cursor.close()
cnx.close()