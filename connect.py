import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Replace with your RDS instance details
host = "your_rds_endpoint"
user = "your_username"
password = "your_password"
database = "your_database_name"

# Establish connection
connection = create_connection(host, user, password, database)

# Create a table
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
) ENGINE = InnoDB
"""
execute_query(connection, create_users_table)

# Insert data
insert_users = """
INSERT INTO users (name, email) 
VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Mike Johnson', 'mike@example.com')
"""
execute_query(connection, insert_users)

# Query data
select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

# Print results
for user in users:
    print(user)

# Close the connection
if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")