# python3 app.py

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
print("MySQL connector installed successfully.")
from datetime import datetime, timedelta

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "port":3306,
    "password": "wcsodw1Mysql",  # Enter your MySQL password here
    "database": "anyFlower",
}

@app.route('/', methods=['GET', 'POST'])
def index():

    query = None  # Initialize query with a default value

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        dollars = request.form.get('dollars')
        signer = request.form.get('signer')
        item_name_dropdown = request.form.get('item_name_dropdown')
        signer_dropdown = request.form.get('signer_dropdown')
        timestamp_range = request.form.get('timestamp_range')

        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert the user's input into the 'ItemDataTable' table
            if item_name and dollars and signer:
                insert_query = "INSERT INTO ItemDataTable (item, dollars, signer, timestamp) VALUES (%s, %s, %s, %s);"
                current_timestamp = datetime.now()
                print(current_timestamp)
                #seven_days_ago = current_timestamp - timedelta(days=7)
                cursor.execute(insert_query, (item_name, dollars, signer, current_timestamp))
                conn.commit()

            # Determine the item and signer values based on the dropdown selection
            if item_name_dropdown:
                item_name = item_name_dropdown
            if signer_dropdown:
                signer = signer_dropdown


            # Insert the user's input into the 'ItemDataTable' table
            if item_name and dollars and signer:
                insert_query = "INSERT INTO ItemDataTable (item, dollars, signer, timestamp) VALUES (%s, %s, %s, %s);"
                current_timestamp = datetime.now()
                cursor.execute(insert_query, (item_name, dollars, signer, current_timestamp))
                conn.commit()

            # Query for total dollars based on timestamp selection
            if timestamp_range == '1_day':
                query = "SELECT DATE(timestamp) AS day, SUM(dollars) AS total FROM ItemDataTable WHERE DATE(timestamp) = CURDATE() GROUP BY day;"
            elif timestamp_range == '1_week':
                # query = "SELECT DATE(timestamp) AS week, SUM(dollars) AS total FROM ItemDataTable WHERE YEARWEEK(timestamp) = YEARWEEK(CURDATE()) GROUP BY week;"
                query = "SELECT YEARWEEK(timestamp, 1) AS week, SUM(dollars) AS total FROM ItemDataTable WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1) GROUP BY week;"

            elif timestamp_range == '1_year':
                query = "SELECT YEAR(timestamp) AS year, SUM(dollars) AS total FROM ItemDataTable WHERE YEAR(timestamp) = YEAR(CURDATE()) GROUP BY year;"

            cursor.execute(query)
            result = cursor.fetchall()

        except mysql.connector.Error as e:
            print(f"Error: {e}")
        # finally:
        #     if cursor:
        #         cursor.close()
        #     if conn:
        #         conn.close()
        return render_template(
            'index.html',
            result=result,
            item_name_dropdown=item_name_dropdown,
            signer_dropdown=signer_dropdown,
        )
    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(debug=True)
