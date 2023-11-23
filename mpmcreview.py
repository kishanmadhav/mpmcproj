# -*- coding: utf-8 -*-
#import required libraries
import rasterio
from rasterio import plot
from matplotlib import pyplot as plt
import numpy as np
%matplotlib inline
import os

# Open red and NIR bands
band4 = rasterio.open(r"C:\Users\KISHAN MADHAV A G\OneDrive\Desktop\mpmc final\LC08_L1TP_042035_20180603_20180615_01_T1_B4_clip.tif")  # red
band5 = rasterio.open(r"C:\Users\KISHAN MADHAV A G\OneDrive\Desktop\mpmc final\LC08_L1TP_042035_20180603_20180615_01_T1_B5_clip.tif")  # NIR

# Generate red and NIR arrays
red = band4.read(1).astype('float64')
nir = band5.read(1).astype('float64')

# Calculate NDVI
ndvi = np.where(
    (nir + red) == 0.,
    0,
    (nir - red) / (nir + red))

# Print NDVI values
print("NDVI Values:")
print(ndvi)

# Define NDVI threshold values for vegetation categories
low_veg_threshold = 0.2
high_veg_threshold = 0.5

# Categorize NDVI values
low_veg = np.where(ndvi < low_veg_threshold, 1, 0)
moderate_veg = np.where((ndvi >= low_veg_threshold) & (ndvi < high_veg_threshold), 1, 0)
high_veg = np.where(ndvi >= high_veg_threshold, 1, 0)

# Print categorized vegetation values
print("\nCategorized Vegetation:")
print(f"Low Vegetation pixels: {np.sum(low_veg)}")
print(f"Moderate Vegetation pixels: {np.sum(moderate_veg)}")
print(f"High Vegetation pixels: {np.sum(high_veg)}")

# Export NDVI image
output_ndvi_path = r"C:\Users\KISHAN MADHAV A G\images\mpmcfinal"
ndviImage = rasterio.open(output_ndvi_path, 'w', driver='GTiff',
                          width=band4.width,
                          height=band4.height,
                          count=1, crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
ndviImage.write(ndvi, 1)
ndviImage.close()

# Plot NDVI image
ndvi = rasterio.open(output_ndvi_path)
fig = plt.figure(figsize=(18, 12))
plot.show(ndvi)
