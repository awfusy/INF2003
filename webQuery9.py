import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

def generate_chart(data, title, x_label='Category', y_label='Average Reviews'):
    sizes = np.array(data['average']) * 100
    # Create a bubble plot
    plt.figure(figsize=(15, 8))
    scatter = plt.scatter(range(len(data['product_category_name'])), data['average'],
                          s=sizes, alpha=0.7, c=data['average'], cmap='viridis')

    # Add labels and title
    plt.xticks(range(len(data['product_category_name'])), data['product_category_name'], rotation=90, ha='right')
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)  # Increase title font size slightly

    # Add a colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Review Score')

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
