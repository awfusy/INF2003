from flask import Flask, render_template
import paramiko
import mysql.connector	
from mysql.connector import connect, Error
import sshtunnel
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pymongo
from prettytable import PrettyTable
import time

app = Flask(__name__)

def generate_bar_chart(data, labels):
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data, color='skyblue')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title('Your Bar Chart Title')
    plt.tight_layout()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64

@app.route('/')
@app.route('/index.html')
def index():
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
        
        connection = mysql.connector.connect(
                user=mysql_user,
                host=mysql_host,
                port=tunnel.local_bind_port,
                password=mysql_password,
                database=mysql_database,
                use_pure=True,  
                        
        )
        print("MySQL Connection Established")

        # Your MySQL query here
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM olist_db.olist_sellers_dataset LIMIT 5;")
        result = cursor.fetchall()
        # print(result)
        # Extract data for the chart (example assumes two columns: id and value)
        chart_labels = [str(row[0]) for row in result]
        chart_data = [row[1] for row in result]
        
        cursor.close()
        connection.close()
        # Close SSH connection
        ssh_client.close()

        # Generate the bar chart
        chart_image = generate_bar_chart(chart_data, chart_labels)

        # Connect to the MongoDB database
        client = pymongo.MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
        db = client["INF2003"]  # Replace with your database name

    return render_template('home/index.html', chart_image=chart_image)


     

if __name__ == "__main__":
    app.run(debug=True)