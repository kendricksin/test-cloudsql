import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt

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

# Create a new table for employee performance
create_performance_table = """
CREATE TABLE IF NOT EXISTS employee_performance (
  id INT AUTO_INCREMENT PRIMARY KEY,
  employee_id INT,
  year INT,
  performance_score FLOAT,
  salary FLOAT,
  FOREIGN KEY (employee_id) REFERENCES users(id)
) ENGINE = InnoDB
"""
execute_query(connection, create_performance_table)

# Insert sample data into employee_performance
insert_performance = """
INSERT INTO employee_performance (employee_id, year, performance_score, salary) 
VALUES 
    (1, 2020, 8.5, 50000),
    (1, 2021, 9.0, 55000),
    (1, 2022, 9.2, 60000),
    (2, 2020, 7.8, 48000),
    (2, 2021, 8.2, 52000),
    (2, 2022, 8.5, 56000),
    (3, 2020, 8.0, 49000),
    (3, 2021, 8.3, 53000),
    (3, 2022, 8.7, 58000)
"""
execute_query(connection, insert_performance)

# Query data
query = """
SELECT u.name, ep.year, ep.performance_score, ep.salary
FROM users u
JOIN employee_performance ep ON u.id = ep.employee_id
ORDER BY u.name, ep.year
"""

# Use pandas to read the query result
df = pd.read_sql(query, connection)

# Close the connection
connection.close()
print("MySQL connection is closed")

# Create a scatter plot
plt.figure(figsize=(10, 6))
for name in df['name'].unique():
    employee_data = df[df['name'] == name]
    plt.scatter(employee_data['performance_score'], employee_data['salary'], label=name)

plt.xlabel('Performance Score')
plt.ylabel('Salary')
plt.title('Employee Performance vs Salary')
plt.legend()

# Save the plot (Repl.it doesn't support plt.show())
plt.savefig('performance_vs_salary.png')
print("Scatter plot saved as 'performance_vs_salary.png'")

# Display the dataframe
print(df)