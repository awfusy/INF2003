import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, title, x_label='Category', y_label='Count'):

    data['state'] = data['state'].str.replace('\r','')
    category_colors = {'bed_bath_table': 'red', 'sports_leisure': 'blue', 'health_beauty': 'green',
                       'telephony': 'purple'}

    plt.figure(figsize=(8, 6))
    for category, color in category_colors.items():
        category_data = data[data['HighestSoldCategory'] == category]
        bars = plt.bar(category_data['state'], category_data['QuantitySold'], color=color, label=category)
        # Determine the maximum label length
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, round(yval, 1), ha='center', va='bottom',
                     fontsize=8)

    max_label_length = max(len(str(label)) for label in data['state'])
    font_size = min(8, 200 / max_label_length)  # You can adjust the divisor for fine-tuning

    plt.xlabel(x_label, fontsize= font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.title(title, fontsize=font_size + 6)  # Increase title font size slightly
    plt.xticks(rotation=20, ha='right', fontsize=font_size)  # Rotate and slant X-axis labels
    plt.legend()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
