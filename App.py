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



import streamlit as st
from PIL import Image

st.set_page_config(page_title="Evolution of snow in the South-West Alps", page_icon=":earth_americas:", layout="wide", initial_sidebar_state="expanded")

@st.cache
def load_image(image_path):
    return Image.open(image_path)

def main():
    st.sidebar.title("Evolution of snow in 2024 in the South-West Alps: Piedmont, Italy")
    
    st.sidebar.write("This program visualizes the evolution of snow in the South-West Alps near Piedmont Italy during 2024 using Sentinel-2 satellite imagery. It consists of an image per month of the year")

    month = st.sidebar.slider("Choose a month", 1, 12, 1, format="%d")
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][month-1]
    st.write(f"You selected: {month_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("RGB or True Color Image")
        st.image(f"Results\RGB\{month_name}_RGB.png", use_column_width=True)
    with col2:
        st.write("False Color Image")  
        st.image(f"Results\FalseColor\{month_name}_FalseColor.png", use_column_width=True)  

    

if __name__ == "__main__":
    main()
