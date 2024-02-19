import os
import imageio
import ipywidgets as widgets
from IPython.display import display

# Get the list of image files in the 'time_maps' folder
image_folder = 'time_maps'
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.png')]
image_files.sort()  # Sort the files by name

# Create a widget to display the images
image_widget = widgets.Image()

# Define a function to update the image
def update_image(change):
    image_path = image_files[change['new']]
    with open(image_path, 'rb') as f:
        image_widget.value = f.read()

# Create an image slider widget
image_slider = widgets.IntSlider(min=0, max=len(image_files) - 1, description='Image:')
image_slider.observe(update_image, 'value')

# Display the initial image
update_image({'new': 0})

# Display the image slider and image widget
display(image_slider)
display(image_widget)
