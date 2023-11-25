import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(data, title, x_label='Category', y_label='Time (Hours)'):
    data = data.T.reset_index()
    data.columns = ['Category', 'Time']

    # Create a grouped bar chart
    plt.figure(figsize=(8, 6))
    data.plot(x='Category', y='Time', kind='bar', color=['skyblue', 'lightcoral'], legend=False)

    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)  # Increase title font size slightly

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

    return image_base64