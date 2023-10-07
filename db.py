
import mysql.connector

# MySQL database configuration
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "wcsodw1Mysql",  # Enter your MySQL password here
#     "database": "anyFlower",  # Change to your desired database name
# }

heroku_db_config = {
    "host": "us-cluster-east-01.k8s.cleardb.net",
    "user": "b18d41c3b2d8db", # username
    "port":3306,
    "password": "e25efe5a",  # Enter your MySQL password here
    "database": "heroku_30ff1240d980ded",
}


# Create a connection to the MySQL server
connection = mysql.connector.connect(**heroku_db_config)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the SQL query to create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS ItemDataTable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    dollars DECIMAL(10, 2) NOT NULL,
    signer VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Table created successfully!")


