# python3 app.py

from flask import Flask, render_template, request, redirect, url_for, redirect
import mysql.connector
print("MySQL connector installed successfully.")

app = Flask(
    __name__,
    static_folder="static",  # 靜態檔案的資料夾名稱
    static_url_path="/"  # 靜態檔案對應的網址路徑
)

app.secret_key = "any string but secret"  # 設定 session 的密鑰


def db_connection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            database="anyFlower",
            password="wcsodw1Mysql",
            charset="utf8"
        )
    except mysql.connector.Error as e:
        print(e)
    return mydb

db = db_connection()

# === #

@app.route('/', methods=['GET', 'POST'])
def index():
    summation = None

    if request.method == 'POST':
        timestamp_range = request.form.get('timestamp_range')
        custom_value = request.form.get('custom_value')


        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()

            if timestamp_range == '1_day':
                # Calculate summation for one day (adjust the timestamp filter accordingly)
                query = "SELECT SUM(dollars) FROM FlowerData WHERE timestamp >= CURDATE();"
            elif timestamp_range == '1_week':
                # Calculate summation for one week (adjust the timestamp filter accordingly)
                query = "SELECT SUM(dollars) FROM FlowerData WHERE timestamp >= CURDATE() - INTERVAL 1 WEEK;"
            elif timestamp_range == '1_year':
                # Calculate summation for one year (adjust the timestamp filter accordingly)
                query = "SELECT SUM(dollars) FROM FlowerData WHERE timestamp >= CURDATE() - INTERVAL 1 YEAR;"
            elif timestamp_range == 'custom':
                # Calculate summation based on a custom value
                query = f"SELECT SUM(dollars) FROM FlowerData WHERE dollars >= {custom_value};"

            cursor.execute(query)
            summation = cursor.fetchone()[0]

        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('index.html', summation=summation)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/")
# def index():
#     # Retrieve and display total dollars for today, this week, this month, and this year
#     # You need to implement these queries based on your database structure
#     today_total = get_total_for_today()
#     week_total = get_total_for_week()
#     month_total = get_total_for_month()
#     year_total = get_total_for_year()
#     return render_template("index.html", today_total=today_total, week_total=week_total, month_total=month_total, year_total=year_total)


