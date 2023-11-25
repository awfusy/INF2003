import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, labels, title, x_label='Category', y_label='Count', top_n=10):
    # Sort data and labels in descending order
    sorted_data, sorted_labels = zip(*sorted(zip(data, labels), reverse=True))

    # Select only the top N items
    top_data = sorted_data[:top_n]
    top_labels = sorted_labels[:top_n]

    plt.figure(figsize=(8, 6))
    plt.bar(top_labels, top_data, color='skyblue')

    # Determine the maximum label length
    max_label_length = max(len(str(label)) for label in top_labels)

    # Adjust font size dynamically based on label length
    font_size = min(8, 200 / max_label_length)  # You can adjust the divisor for fine-tuning

    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.title(title, fontsize=font_size + 6)  # Increase title font size slightly
    plt.xticks(rotation=20, ha='right', fontsize=font_size)  # Rotate and slant X-axis labels

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
