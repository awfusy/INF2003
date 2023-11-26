from flask import Flask, render_template
import paramiko
import mysql.connector
from mysql.connector import connect, Error
import sshtunnel
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pymongo
from dash import Dash, dcc, html, Output
from dash_table import DataTable
from dash.dependencies import Input, State
import pandas as pd
import webQuery1 as q1
import webQuery2 as q2
import webQuery3 as q3
import webQuery4 as q4
import webQuery5 as q5
import webQuery6 as q6
import webQuery7 as q7
import webQuery8 as q8
import webQuery9 as q9
import webQuery10 as q10
from flask import request, session, redirect, url_for
import secrets
from flask import request

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)  # Generate a 32-character (16 bytes) hexadecimal secret key

@app.route('/', methods=['GET', 'POST'])
def login():
    # SSH Configuration
    ssh_host = '35.212.230.135'
    ssh_port = 22
    ssh_user = 'dev'
    ssh_password = 'Inf2003dev'

    # MySQL Configuration
    mysql_host = 'localhost'  # or the IP address of your MySQL server
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = 'Inf2003root'
    mysql_database = 'olist_db'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

        # Establish SSH connection
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
            print("SSH Connection Established")

            # Establish MySQL connection through SSH tunnel
            with sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(mysql_host, mysql_port),
            ) as tunnel:
                print("SSH Tunnel Established")
                print(tunnel)

                # MySQL Connection
                with mysql.connector.connect(
                        user=mysql_user,
                        host=mysql_host,
                        port=tunnel.local_bind_port,
                        password=mysql_password,
                        database=mysql_database,
                        use_pure=True,
                ) as connection:
                    print("MySQL Connection Established")

                    # SQL Query to check if the username and password exist in the accounts_dataset table
                    query = f"SELECT * FROM accounts_dataset WHERE username = '{username}' AND password = '{password}'"
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        result = cursor.fetchone()
                        print(result)

                    if result:
                        # Authentication successful, store the username in the session
                        session['username'] = username
                        return redirect(url_for('index'))  # Redirect to /index route
                    else:
                        # Authentication failed, show an error message
                        error = 'Invalid username or password'
                        return render_template('login/login.html', error=error)

    return render_template('login/login.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    # SSH Configuration
    ssh_host = '35.212.230.135'
    ssh_port = 22
    ssh_user = 'dev'
    ssh_password = 'Inf2003dev'

    # MySQL Configuration
    mysql_host = 'localhost'  # or the IP address of your MySQL server
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = 'Inf2003root'
    mysql_database = 'olist_db'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        staff_role = request.form['staff_role']                

        # Establish SSH connection
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
            print("SSH Connection Established")

            # Establish MySQL connection through SSH tunnel
            with sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(mysql_host, mysql_port),
            ) as tunnel:
                print("SSH Tunnel Established")
                print(tunnel)

                # MySQL Connection
                with mysql.connector.connect(
                        user=mysql_user,
                        host=mysql_host,
                        port=tunnel.local_bind_port,
                        password=mysql_password,
                        database=mysql_database,
                        use_pure=True,
                ) as connection:
                    print("MySQL Connection Established")
                    insert_query = "INSERT INTO accounts_dataset (username, password, staff_role) VALUES (%s, %s, %s)"
                    with connection.cursor() as cursor:
                        cursor = connection.cursor()
                                    
                        values = (username, password, staff_role)
                        
                        cursor.execute(insert_query, values)
                        
                        connection.commit()
                        
                        cursor.close()
                        connection.close()
        
        return "Account created successfully"    
    
    return render_template('admin/accountCreation.html')


@app.route('/updateAccount', methods=['GET', 'POST'])
def updateAccount():
    if request.method == 'POST':
        # Get the form data
        new_userid = request.form.get('current_userid')        
        new_username = request.form.get('username')
        new_password = request.form.get('password')
        new_staff_role = request.form.get('staffRole')

        # SSH Configuration
        ssh_host = '35.212.230.135'
        ssh_port = 22
        ssh_user = 'dev'
        ssh_password = 'Inf2003dev'

        # MySQL Configuration
        mysql_host = 'localhost'  # or the IP address of your MySQL server
        mysql_port = 3306
        mysql_user = 'root'
        mysql_password = 'Inf2003root'
        mysql_database = 'olist_db'
        
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)

            with sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(mysql_host, mysql_port),
            ) as tunnel:

                with mysql.connector.connect(
                        user=mysql_user,
                        host=mysql_host,
                        port=tunnel.local_bind_port,
                        password=mysql_password,
                        database=mysql_database,
                        use_pure=True,
                ) as connection:
                    # Update the account details in the database
                    update_query = (
                        "UPDATE accounts_dataset SET username=%s, password=%s, staff_role=%s WHERE user_id=%s"
                    )

                    with connection.cursor() as cursor:
                        cursor.execute(update_query, (new_username, new_password, new_staff_role, new_userid))
                        connection.commit()     
                    select_query = "SELECT * FROM accounts_dataset"
                    with connection.cursor() as cursor:
                        cursor.execute(select_query)
                        accounts_data = cursor.fetchall()
   
        return render_template('admin/accountUpdate.html', accounts=accounts_data)

    elif request.method == 'GET':
        # SSH Configuration
        ssh_host = '35.212.230.135'
        ssh_port = 22
        ssh_user = 'dev'
        ssh_password = 'Inf2003dev'

        # MySQL Configuration
        mysql_host = 'localhost'  # or the IP address of your MySQL server
        mysql_port = 3306
        mysql_user = 'root'
        mysql_password = 'Inf2003root'
        mysql_database = 'olist_db'

        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
        print("SSH Connection Established")
        # Display the account details
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)

            with sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(mysql_host, mysql_port),
            ) as tunnel:

                with mysql.connector.connect(
                        user=mysql_user,
                        host=mysql_host,
                        port=tunnel.local_bind_port,
                        password=mysql_password,
                        database=mysql_database,
                        use_pure=True,
                ) as connection:
                    # Fetch data from accounts_dataset
                    select_query = "SELECT * FROM accounts_dataset"
                    with connection.cursor() as cursor:
                        cursor.execute(select_query)
                        accounts_data = cursor.fetchall()

        return render_template('admin/accountUpdate.html', accounts=accounts_data)

@app.route('/deleteAccount', methods=['POST'])
def deleteAccount():
    if request.method == 'POST':
        user_id_to_delete = request.form.get('user_id_to_delete')
        # SSH Configuration
        ssh_host = '35.212.230.135'
        ssh_port = 22
        ssh_user = 'dev'
        ssh_password = 'Inf2003dev'

        # MySQL Configuration
        mysql_host = 'localhost'  # or the IP address of your MySQL server
        mysql_port = 3306
        mysql_user = 'root'
        mysql_password = 'Inf2003root'
        mysql_database = 'olist_db'

        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
        print("SSH Connection Established")
        
        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)

            with sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_user,
                    ssh_password=ssh_password,
                    remote_bind_address=(mysql_host, mysql_port),
            ) as tunnel:

                with mysql.connector.connect(
                        user=mysql_user,
                        host=mysql_host,
                        port=tunnel.local_bind_port,
                        password=mysql_password,
                        database=mysql_database,
                        use_pure=True,
                ) as connection:
                    # Delete the account from the database
                    delete_query = "DELETE FROM accounts_dataset WHERE user_id = %s"

                    with connection.cursor() as cursor:
                        cursor.execute(delete_query, (user_id_to_delete,))
                        connection.commit()

        # Redirect to the account update page after deletion
        return redirect(url_for('updateAccount'))
    
@app.route('/index')
def index():    
    # Check if the user is logged in
    if 'username' in session:
        # SSH Configuration
        ssh_host = '35.212.230.135'
        ssh_port = 22
        ssh_user = 'dev'
        ssh_password = 'Inf2003dev'

        # MySQL Configuration
        mysql_host = 'localhost'  # or the IP address of your MySQL server
        mysql_port = 3306
        mysql_user = 'root'
        mysql_password = 'Inf2003root'
        mysql_database = 'olist_db'

        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
        print("SSH Connection Established")

        # Establish MySQL connection through SSH tunnel
        with sshtunnel.SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(mysql_host, mysql_port),
        ) as tunnel:
            print("SSH Tunnel Established")
            print(tunnel)

            # MySQL Connection
            connection = mysql.connector.connect(
                user=mysql_user,
                host=mysql_host,
                port=tunnel.local_bind_port,
                password=mysql_password,
                database=mysql_database,
                use_pure=True,
            )
            print("MySQL Connection Established")

        
            # Query 1: Revenue generated by category
            q1_query = """
                SELECT p.product_category_name,COUNT(DISTINCT oi.order_id) AS Num_orders,SUM(oi.price) AS Revenue
                FROM olist_order_items_dataset oi
                JOIN olist_products_dataset p ON oi.product_id = p.product_id
                JOIN olist_orders_dataset o ON oi.order_id = o.order_id
                WHERE o.order_status <> 'canceled' AND o.order_delivered_customer_date IS NOT NULL
                GROUP BY p.product_category_name
                ORDER BY Revenue DESC LIMIT 10;
            """
            q1_df = pd.read_sql_query(q1_query, connection)

            # Query 2: Number of 5-star reviews by category
            q2_query = """
                SELECT P.product_category_name, COUNT(R.review_score) AS Num_5_star_reviews
                FROM olist_order_reviews_dataset R
                JOIN olist_order_items_dataset I ON R.order_id = I.order_id
                JOIN olist_products_dataset P ON I.product_id = P.product_id
                WHERE R.review_score = 5
                GROUP BY P.product_category_name
                ORDER BY Num_5_star_reviews DESC LIMIT 10;
            """
            q2_df = pd.read_sql_query(q2_query, connection)
            q2_chart_labels = q2_df['product_category_name'].tolist()
            q2_chart_data = q2_df['Num_5_star_reviews'].tolist()

            # Query 3: Which category is the most popular by geolocation?
            q3_query = """
                WITH StateCategorySales AS (
                SELECT
                    c.customer_state AS state,
                    p.product_category_name AS category,
                    COUNT(o.order_id) AS QuantitySold
                FROM
                    olist_orders_dataset o
                    JOIN olist_order_items_dataset oi ON o.order_id = oi.order_id
                    JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
                    JOIN olist_products_dataset p ON oi.product_id = p.product_id
                WHERE
                    o.order_status = 'delivered'
                GROUP BY
                    c.customer_state, p.product_category_name
                )
                SELECT
                    scs.state AS state,
                    scs.category AS HighestSoldCategory,
                    scs.QuantitySold
                FROM
                    StateCategorySales scs
                JOIN (
                    SELECT
                        state,
                        MAX(QuantitySold) AS MaxQuantitySold
                    FROM
                        StateCategorySales
                    GROUP BY
                        state
                ) maxSales ON scs.state = maxSales.state AND scs.QuantitySold = maxSales.MaxQuantitySold
                ORDER BY
                    scs.QuantitySold DESC, scs.state;
            """
            q3_df = pd.read_sql_query(q3_query, connection)

            # Query 4: Frequently Bought items
            q4_query = """
                SELECT p.product_category_name, COUNT(oi.order_id) AS order_count
                FROM olist_order_items_dataset oi
                JOIN olist_products_dataset p ON oi.product_id = p.product_id
                GROUP BY p.product_category_name
                ORDER BY order_count DESC;
            """
            q4_df = pd.read_sql_query(q4_query, connection)
            q4_chart_labels = q4_df['product_category_name'].tolist()
            q4_chart_data = q4_df['order_count'].tolist()

            #query 5:
            q5_query = """
                        SELECT
                    c.customer_city,
                    c.customer_state,
                    ROUND(SUM(oi.price),2) AS TotalRevenue
                FROM
                    olist_orders_dataset o
                JOIN
                    olist_order_items_dataset oi ON o.order_id = oi.order_id
                JOIN
                    olist_customers_dataset c ON o.customer_id = c.customer_id
                WHERE
                    o.order_status = 'delivered'
                    AND o.order_delivered_customer_date IS NOT NULL
                GROUP BY
                    c.customer_city, c.customer_state
                ORDER BY
                    TotalRevenue DESC limit 10;
            """
            q5_df = pd.read_sql_query(q5_query, connection)

            # Query 6: Payment Type Distribution
            q6_query = """
                SELECT payment_type, COUNT(order_id) AS payment_count
                FROM olist_order_payments_dataset
                GROUP BY payment_type
                ORDER BY payment_count DESC;
            """
            q6_df = pd.read_sql_query(q6_query, connection)
            q6_chart_labels = q6_df['payment_type'].tolist()
            q6_chart_data = q6_df['payment_count'].tolist()
            # Query 7: Average completion of processing time/ shipping time
            q7_query = """
                    SELECT
                    AVG(TIMESTAMPDIFF(SECOND, order_purchase_timestamp , order_approved_at))/3600 AS average_processing_time,
                    AVG(TIMESTAMPDIFF(SECOND, order_delivered_carrier_date, order_delivered_customer_date))/3600 AS average_shipping_time
                FROM
                    olist_db.olist_orders_dataset
                WHERE
                    order_status = 'delivered';
            """
            q7_df = pd.read_sql_query(q7_query, connection)

            # Query 8: Average delivery time and freight fee
            q8_query = """
                SELECT
                    ROUND(AVG(average_delivery_time),2) AS overall_average_delivery_time,
                    ROUND(AVG(average_delivery_fee),2) AS overall_average_delivery_fee
                FROM (
                    SELECT
                        OI.order_id,
                        AVG(TIMESTAMPDIFF(SECOND, O.order_delivered_carrier_date, O.order_delivered_customer_date) / 3600) AS average_delivery_time,
                        AVG(OI.freight_value) AS average_delivery_fee
                    FROM olist_order_items_dataset OI
                    JOIN olist_orders_dataset O ON OI.order_id = O.order_id
                    WHERE O.order_status = 'delivered'
                    GROUP BY OI.order_id
                ) AS subquery;
            """
            q8_df = pd.read_sql_query(q8_query, connection)
            q8_data1 = q8_df['overall_average_delivery_time'].tolist()
            q8_data2 = q8_df['overall_average_delivery_fee'].tolist()

            # Query 9: Average customer reviews score on product category
            q9_query ="""
            SELECT P.product_category_name, AVG(R.review_score) AS average
                FROM olist_db.olist_order_reviews_dataset R
                JOIN olist_db.olist_order_items_dataset I on R.order_id = I.order_id
                JOIN olist_db.olist_products_dataset P on I.product_id = P.product_id
                GROUP BY P.product_category_name
                ORDER BY average DESC;
            """
            q9_df = pd.read_sql_query(q9_query, connection)

            # Query 10: Categories with the most sellers
            q10_query="""
            SELECT P.product_category_name, COUNT(DISTINCT S.seller_id)
                FROM olist_db.olist_products_dataset P
                JOIN olist_db.olist_order_items_dataset I ON P.product_id = I.product_id
                JOIN olist_db.olist_sellers_dataset S ON I.seller_id = S.seller_id
                GROUP BY product_category_name
                ORDER BY COUNT(DISTINCT S.seller_id) DESC
                LIMIT 10;

            """
            q10_df = pd.read_sql_query(q10_query, connection)

            # Generate the bar charts
            q1_chart_image = q1.generate_chart(q1_df, 'Revenue generated by category')
            q2_chart_image = q2.generate_chart(q2_chart_data, q2_chart_labels, 'Which product category appears most in 5* review?')
            q3_chart_image = q3.generate_chart(q3_df, 'Which category is the most popular by geolocation?')
            q4_chart_image = q4.generate_chart(q4_chart_data, q4_chart_labels, 'Frequently Bought category', top_n=10)
            q5_chart_image = q5.generate_chart(q5_df, 'Most revenue by location')
            q6_chart_image = q6.generate_chart(q6_chart_data, q6_chart_labels, 'Payment Type Distribution')
            q7_chart_image = q7.generate_chart(q7_df, 'Average completion of processing time/ shipping time')
            q8_chart_image = q8.generate_chart(q8_data1, q8_data2, ['Average Delivery Time and Fee'], 'Average Delivery Time and Fee')
            q9_chart_image = q9.generate_chart(q9_df, 'Average customer reviews score on product category')
            q10_chart_image = q10.generate_chart(q10_df, 'Categories with the most sellers')        
            return render_template('home/index.html',
                    q1_chart_image=q1_chart_image,
                    q2_chart_image=q2_chart_image,
                    q3_chart_image=q3_chart_image,
                    q4_chart_image=q4_chart_image,
                    q5_chart_image=q5_chart_image,
                    q6_chart_image=q6_chart_image,
                    q7_chart_image=q7_chart_image,
                    q8_chart_image=q8_chart_image,
                    q9_chart_image=q9_chart_image,
                    q10_chart_image=q10_chart_image,
                    username=session['username']
                    )
    else:
        return redirect(url_for('/'))        

if __name__ == '__main__':
    app.run(debug=True)
