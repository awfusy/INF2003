import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, labels, title):
    # Sort data and labels in descending order
    sorted_data, sorted_labels = zip(*sorted(zip(data, labels), reverse=True))

    plt.figure(figsize=(10, 8))
    plt.pie(sorted_data, labels=sorted_labels, autopct='%1.1f%%', startangle=140, explode=(0.1, 0, 0, 0, 0), shadow=True)

    # Adjust font size dynamically based on label length
    font_size = min(8, 200 / max(len(str(label)) for label in sorted_labels))

    plt.title(title, fontsize=font_size + 6)  # Increase title font size slightly

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png',bbox_inches='tight')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
