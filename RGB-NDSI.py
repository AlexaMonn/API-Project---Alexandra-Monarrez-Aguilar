# NAME:
# Evolution of snow in the South-West AlpsL: Piedmont, Italy
#
# AUTHOR:
# Alexandra Monarrez Aguilar
#  
# PURPOSE:  
# Visualize the evolution of snow in the South-West Alps near Piedmont Italy during 2024 using Sentinel-2 satellite imagery
# in RGB (True Color) and False Color images.
#
# The program consists of two main Python files.
# The programs where separated for a better organization and more organic understanding of the programs:
# 1- RGB-NDSI.py: This script processes the Sentinel-2 bands to create RGB and False Color images for each month of the year.
#                 First, the images where downloaded from Copernicus. To decide what day of the year for each month in 2024
#                 to download the images, the least cloud coverage was considered. As well as the closest day of the year
#                 to keep the closest uniformity of information. 
# 
#                 After downloading the files of each month, only bands 2, 3, 4, 8, and 11 where selected to create the stack 
#                 of bands into a single tif file to process it. RGB-NDSI.py is a program that does the stack using the images
#                 of the bands saved in a folder for each month, which can be seen in the "Data" folder. The stack created
#                 for each month is saved in the "Results" folder. For example: "April.tif". Then, using the stacks, the program
#                 has code for creating RGB and False Color images for each month. The RGB image is created using bands 4, 3, and 2,
#                 which as being saved as a stack become bands 3, 2, and 1, respectively. The False Color image is created using
#                 bands 8, 3, and 2, which as being saved as a stack become bands 4, 3, and 2, respectively. The images are saved   
#                 in the "Results" folder. There is one folder dor RGB images and another for False Color images. Additionally, 
#                 a Gamma correction and brightness was applied to the RGB images to enhance the colors.
#
# 2-      App.py: This script is the Streamlit application that visualizes the images created in RGB-NDSI.py. The application has a 
#                 slider to visualize the month selected in RGB and False color obtianed in "RGB-NDSI.py".    
# 
#  CATEGORY:  
#  Color Image Processing.  
#  
#  CALLING SEQUENCE:  
#  Use the link provided in the README.txt file and copy paste the URL in the browser to visualize the program.  
#  Additionally, if the user wants to run the program locally, the user has to follow the next steps:
#  1- Extract the ZIP file.
#  2- Install Python.
#  3- Set up a virtual environment to navigate to the extracted project directory. "python -m venv venv".
#  4- Activate the virtual environment. "venv\Scripts\activate" in Windows or "source venv/bin/activate" in MacOS/Linux.
#  5- Install the required libraries found in "RGB-NDSI.py" and "App.py".
#  6- Run the "RGB-NDSI.py" script to process the images.
#  7- Run the "App.py". and run the app in the terminal using "streamlit run App.py".
#  
#  INPUTS:  
#  DATA folder: Contains the images of the bands downloaded from Copernicus for each month of the year.
#  
#  OUTPUTS:  
#  RESULTS folder: Contains the stack images in tif files of the bands of each month obtained from the "DATA" folder. 
#                  Contains the folders "RGB" and "FalseColor" which contain their respective images for each month
#                  of the year in png format.
#  App.py: Streamlit application that visualizes the images created in RGB-NDSI.py.
#  
#  SIDE EFFECTS:  
#  None.  
#  
#  RESTRICTIONS:  
#  None.  
#  
#  PROCEDURE:  
#  If the user uses the link provided in the README.txt file, the user will be able to visualize the program.
#  If the user wants to run the program locally, the user has to follow the steps mentioned in the "CALLING SEQUENCE" section.  
#  
#  MODIFICATION HISTORY:  
#  1- "RGB-NDSI.py":
#  - Copernicus Open Access Hub. (n.d.). Sentinel-2 Level-2A data browser. Retrieved December 2, 2024, from https://browser.dataspace.copernicus.eu/
#   (Used to download Sentinel-2 images for the South-West Alps near Piedmont Italy during 2024.)
#  - Mapbox. (n.d.). Rasterio documentation. Retrieved December 7, 2024, from https://rasterio.readthedocs.io/en/stable/topics/index.html 
#   (Includes code examples and technical guidelines for working with geospatial raster data using the Rasterio library.)
#  - SatMapper. (n.d.). RGB image creation tutorial. Retrieved December 23, 2024, from https://www.satmapper.hu/en/rgb-images/
#   (Used and modified the code to apply brightness and gamma correction to the RGB images.)
#  2- "App.py":
#  - Streamlit. (n.d.). Get started with Streamlit. Retrieved December 26, 2025, from https://docs.streamlit.io/get-started
#   (Used to create the Streamlit application for visualizing the images).


#%% Stacking the sentinel bands into a single tif file with bands 2, 3, 4, 8, and 11
import os
import rasterio
import numpy as np
from rasterio.merge import merge
from matplotlib import pyplot as plt

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the base directory relative to the script
base_dir = os.path.join(script_dir, "data", "Sentinel")
output_dir = os.path.join(script_dir, "Results")

# List of bands to process
bands = ["B2.jp2", "B3.jp2", "B4.jp2", "B8.jp2", "B11.jp2"]

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through each month folder
for month_folder in sorted(os.listdir(base_dir)):
    month_path = os.path.join(base_dir, month_folder)
    
    if not os.path.isdir(month_path):
        continue  # Skip files, only process directories
    
    band_paths = []
    for band_file in bands:
        band_path = os.path.join(month_path, band_file)
        if os.path.exists(band_path):
            band_paths.append(band_path)
        else:
            print(f"Warning: {band_file} not found in {month_folder}")
    
    if len(band_paths) != len(bands):
        print(f"Skipping {month_folder} due to missing bands")
        continue
    
    # Read the bands and write them into a single multi-band TIFF
    output_tiff = os.path.join(output_dir, f"{month_folder}.tif")
    
    with rasterio.open(band_paths[0]) as src0:
        meta = src0.meta
    
    # Update metadata for multi-band TIFF
    meta.update(count=len(bands))
    
    with rasterio.open(output_tiff, 'w', **meta) as dst:
        for idx, band_path in enumerate(band_paths, start=1):
            with rasterio.open(band_path) as src:
                dst.write(src.read(1), idx)
    
    print(f"Created {output_tiff}")

print("Processing complete!")

#%% Converting images to RGB (True-Color) and NDSI (Normalized Difference Snow Index)

# Define paths
input_dir = "./Results"  # Directory containing the multi-band TIFFs
output_dir = "./Results/RGB"  # Directory to save RGB images

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to normalize band data to [0, 1]
def normalize_band(band):
    band_min, band_max = band.min(), band.max()
    return (band - band_min) / (band_max - band_min)

# Function to apply brightness and gamma correction
def apply_brightness_gamma(rgb_image, brightness_factor=1, gamma=2):
    # Apply brightness scaling
    brightened = np.clip(rgb_image * brightness_factor, 0, 1)
    # Apply gamma correction
    corrected = np.power(brightened, 1 / gamma)
    return corrected

# Process each multi-band TIFF
for tiff_file in sorted(os.listdir(input_dir)):
    if tiff_file.endswith(".tif"):
        tiff_path = os.path.join(input_dir, tiff_file)
        output_image = os.path.join(output_dir, tiff_file.replace(".tif", "_RGB.png"))
        
        with rasterio.open(tiff_path) as src:
            # Read the bands: Red (3), Green (2), Blue (1)
            red = src.read(3)
            green = src.read(2)
            blue = src.read(1)
        
        # Normalize bands to [0, 1]
        red_normalized = normalize_band(red)
        green_normalized = normalize_band(green)
        blue_normalized = normalize_band(blue)
        
        # Stack bands to create an RGB image
        rgb_image = np.stack([red_normalized, green_normalized, blue_normalized], axis=-1)
        
        # Apply brightness and gamma correction
        brightness_factor = 1.2  # Adjust as per SatMapper-like approach
        gamma = 2.2
        rgb_image_corrected = apply_brightness_gamma(rgb_image, brightness_factor, gamma)
        
        # Display the RGB image
        plt.figure(figsize=(10, 10))
        plt.imshow(rgb_image_corrected)
        plt.title(f"True-Color Image (Corrected): {tiff_file}")
        plt.axis("off")
        plt.show()
        
        # Save the RGB image as PNG
        plt.imsave(output_image, rgb_image_corrected)
        print(f"Saved SatMapper-like RGB image: {output_image}")

print("Processing complete!")

#%% Calculating the NDSI

# Define paths
input_dir = "./Results"  # Directory containing the multi-band TIFFs
output_dir = "./Results/FalseColor"  # Directory to save false color images

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to normalize band data to [0, 1]
def normalize_band(band):
    band_min, band_max = band.min(), band.max()
    return (band - band_min) / (band_max - band_min)

# Process each multi-band TIFF
for tiff_file in sorted(os.listdir(input_dir)):
    if tiff_file.endswith(".tif"):
        tiff_path = os.path.join(input_dir, tiff_file)
        output_image = os.path.join(output_dir, tiff_file.replace(".tif", "_FalseColor.png"))
        
        with rasterio.open(tiff_path) as src:
            # Read the bands: NIR (4), Red (3), Green (2)
            nir = src.read(4)  # Band 8 (Near-Infrared)
            red = src.read(3)  # Band 4 (Red)
            green = src.read(2)  # Band 3 (Green)
        
        # Normalize bands to [0, 1] for visualization
        nir_normalized = normalize_band(nir)
        red_normalized = normalize_band(red)
        green_normalized = normalize_band(green)
        
        # Stack bands to create a false-color composite
        false_color_image = np.stack([nir_normalized, red_normalized, green_normalized], axis=-1)
        
        # Save the false color image as PNG
        plt.figure(figsize=(10, 10))
        plt.imshow(false_color_image)
        plt.title(f"False Color Composite: {tiff_file}")
        plt.axis("off")
        plt.show()
        
        # Save the RGB image as PNG
        plt.imsave(output_image, false_color_image)
        print(f"Saved SatMapper-like RGB image: {output_image}")

print("Processing complete!")

