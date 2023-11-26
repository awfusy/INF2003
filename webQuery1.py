import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, title, x_label='Category', y_label='Revenue'):
    labels = data['product_category_name']
    revenue_values = data['Revenue']
    order_values = data['Num_orders']

    # Sort data and labels based on revenue in descending order
    sorted_data, sorted_labels = zip(*sorted(zip(revenue_values, labels), reverse=True))
    sorted_orders = [order_values[labels == label].values[0] for label in sorted_labels]

    plt.figure(figsize=(12, 6))

    # Plotting revenue
    plt.bar(sorted_labels, sorted_data, color='skyblue', label='Revenue')

    # Plotting number of orders as a line plot on the secondary axis
    ax2 = plt.gca().twinx()
    ax2.plot(sorted_labels, sorted_orders, color='orange', marker='o', label='Number of Orders')

    plt.xlabel(x_label, fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.title(title, fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.legend(loc='upper left', bbox_to_anchor=(0.7, 1.0), fontsize=8)

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
