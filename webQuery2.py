import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_bar_chart(data, labels, title):
    # Sort data and labels in descending order
    sorted_data, sorted_labels = zip(*sorted(zip(data, labels), reverse=True))

    plt.figure(figsize=(8, 6))
    plt.bar(sorted_labels, sorted_data, color='skyblue')

    # Determine the maximum label length
    max_label_length = max(len(str(label)) for label in sorted_labels)

    # Adjust font size dynamically based on label length
    font_size = min(8, 200 / max_label_length)  # You can adjust the divisor for fine-tuning

    plt.xlabel('Category', fontsize=font_size)
    plt.ylabel('Count', fontsize=font_size)
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
