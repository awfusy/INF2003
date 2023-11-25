import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, title, x_label='Number of Sellers', y_label='Number of Sellers per Product Category'):
    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.barh(data['product_category_name'], data['COUNT(DISTINCT S.seller_id)'], color='skyblue')

    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(axis='x')

    # Display the count values on the bars
    for index, value in enumerate(data['COUNT(DISTINCT S.seller_id)']):
        plt.text(value, index, str(value))

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64