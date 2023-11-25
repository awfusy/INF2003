import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, title, x_label='Customer City', y_label='Total Revenue'):
    data['location'] = (data['customer_city'] + ' ' + data['customer_state']).str.replace('\r', '')
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(data['location'], data['TotalRevenue'], c='blue', marker='o', label='Total Revenue')

    for i, txt in enumerate(data['TotalRevenue']):
        plt.annotate(f'{txt:.2f}', (data['location'][i], data['TotalRevenue'][i]), textcoords="offset points",
                     xytext=(0, 5), ha='center', fontsize=8)

    plt.plot(data['location'], data['TotalRevenue'], linestyle='-', color='gray', linewidth=0.5)

    max_label_length = max(len(str(label)) for label in data['customer_city'])
    font_size = min(8, 200 / max_label_length)  # You can adjust the divisor for fine-tuning

    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.title(title, fontsize=font_size + 6)  # Increase title font size slightly
    plt.xticks(rotation=20, ha='right', fontsize=font_size)  # Rotate and slant X-axis labels
    plt.grid(axis='y')
    plt.legend()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64