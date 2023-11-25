import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_dual_bar_chart(data1, data2, labels, title, x_label='Metric', y_label1='Average Delivery Time(hours)', y_label2='Average Delivery Fee($)'):
    # Sort labels in descending order
    sorted_labels = sorted(labels, reverse=True)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label1, color=color)
    ax1.bar(sorted_labels, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel(y_label2, color=color)
    ax2.bar(sorted_labels, data2, color=color, alpha=0.5)
    ax2.tick_params(axis='y', labelcolor=color)

    # Adjust y-axis scale for better visualization
    max_data1 = max(data1)
    max_data2 = max(data2)
    max_value = max(max_data1, max_data2)
    ax1.set_ylim(0, max_value * 1.2)
    ax2.set_ylim(0, max_value * 1.2)

    fig.tight_layout()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64
