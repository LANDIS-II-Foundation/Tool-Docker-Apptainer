# -*- coding: utf-8 -*-
"""
Created on Fri May  2 10:47:33 2025

@author: Clement + Claude Haiku

This script is used to clip all of the rasters present on
https://github.com/LANDIS-II-Foundation/Extension-Social-Climate-Fire/tree/master/Testing/Core8-SocialClimateFire4.0
in order to make them compatible with the rest of the test files (who have
different origins).
"""

import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
import tempfile
import shutil
from matplotlib.colors import LinearSegmentedColormap
from rasterio.transform import rowcol
from rasterio.mask import mask
from rasterio.windows import from_bounds

def crop_raster_to_reference(reference_raster_path, input_raster_path, output_raster_path):
    """
    Crop a raster to the extent of a reference raster.

    Args:
        reference_raster_path (str): Path to the reference raster
        input_raster_path (str): Path to the raster to be cropped
        output_raster_path (str): Path where the cropped raster will be saved
    """
    # Read the reference raster to get its extent
    with rasterio.open(reference_raster_path) as reference_src:
        reference_bounds = reference_src.bounds
        print(f"Reference raster bounds: {reference_bounds}")

    # Open the input raster
    with rasterio.open(input_raster_path) as src:
        # Calculate the window to clip to reference extent
        window = from_bounds(
            reference_bounds.left, 
            reference_bounds.bottom, 
            reference_bounds.right, 
            reference_bounds.top, 
            src.transform
        )

        # Read the data in the window
        window_data = src.read(window=window)

        # Calculate the transform for the window
        window_transform = rasterio.windows.transform(window, src.transform)

        # Update metadata for the output
        out_meta = src.meta.copy()
        out_meta.update({
            'height': window_data.shape[1],
            'width': window_data.shape[2],
            'transform': window_transform
        })

        # Write the cropped data
        with rasterio.open(output_raster_path, 'w', **out_meta) as dst:
            dst.write(window_data)

    print(f"Cropped raster saved to: {output_raster_path}")
    

# Set these paths to your actual data
os.chdir(r"D:\OneDrive - UQAM\1 - Projets\Post-Doc - Docker and Apptainer Linux v8\Tool-Docker-Apptainer\Testing_files\TestPnET_AllExtension\inputs\disturbances\landUsePlus")
reference_raster_path = "../../core/ecoregion.img"
input_folder = "./"

# Step 1: Read the reference raster with Rasterio
with rasterio.open(reference_raster_path) as reference_src:
    reference_data = reference_src.read(1)  # Read the first band
    reference_meta = reference_src.meta.copy()
    reference_transform = reference_src.transform
    reference_crs = reference_src.crs
    reference_bounds = reference_src.bounds

    print("Reference Raster Properties:")
    print(f"  Transform: {reference_transform}")
    print(f"  Origin: ({reference_transform[2]}, {reference_transform[5]})")
    print(f"  Pixel Size: ({reference_transform[0]}, {reference_transform[4]})")
    print(f"  Dimensions: {reference_src.width} x {reference_src.height}")
    print(f"  Bounds: {reference_bounds}")
    print(f"  CRS: {reference_crs}")

# Step 2: Read all rasters in the input folder
raster_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) 
                if f.endswith(('.tif', '.tiff', '.img', '.jp2'))]

if not raster_files:
    print(f"No raster files found in {input_folder}")
else:
    for i in range(0, len(raster_files)):
        # Take the first raster for demonstration
        first_raster_path = raster_files[i]
        first_raster_name = os.path.basename(first_raster_path)
    
        print(f"\nProcessing first raster: {first_raster_name}")
    
        # Read the first raster
        with rasterio.open(first_raster_path) as src:
            first_data = src.read(1)  # Read the first band
            first_meta = src.meta.copy()
            first_transform = src.transform
            first_bounds = src.bounds
    
            print("Original First Raster Properties:")
            print(f"  Transform: {first_transform}")
            print(f"  Origin: ({first_transform[2]}, {first_transform[5]})")
            print(f"  Pixel Size: ({first_transform[0]}, {first_transform[4]})")
            print(f"  Dimensions: {src.width} x {src.height}")
            print(f"  Bounds: {first_bounds}")
            print(f"  CRS: {src.crs}")
    
            # Step 3: Create a new transform with the reference origin but keeping the original pixel size
            # The transform is in the form (pixel_width, row_rotation, x_origin, column_rotation, pixel_height, y_origin)
            new_transform = rasterio.transform.Affine(
                reference_transform[0],  # Keep original pixel width
                first_transform[1],  # Keep original row rotation
                reference_transform[2],  # Use reference x_origin
                first_transform[3],  # Keep original column rotation
                reference_transform[4],  # Keep original pixel height
                reference_transform[5]   # Use reference y_origin
            )
    
            print("\nNew Transform for First Raster:")
            print(f"  Transform: {new_transform}")
            print(f"  Origin: ({new_transform[2]}, {new_transform[5]})")
            print(f"  Pixel Size: ({new_transform[0]}, {new_transform[4]})")
    
            # Create a temporary file with the new transform
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_output = os.path.join(tmpdirname, first_raster_name)
    
                # Update metadata with new transform
                first_meta.update({
                    'transform': new_transform
                })
    
                # Write the data with the new transform
                with rasterio.open(temp_output, 'w', **first_meta) as dst:
                    dst.write(first_data, 1)
    
                # Read the transformed raster for plotting
                with rasterio.open(temp_output) as transformed_src:
                    transformed_data = transformed_src.read(1)
                    transformed_transform = transformed_src.transform
                    transformed_bounds = transformed_src.bounds
    
                    print("\nTransformed First Raster Properties:")
                    print(f"  Transform: {transformed_transform}")
                    print(f"  Origin: ({transformed_transform[2]}, {transformed_transform[5]})")
                    print(f"  Pixel Size: ({transformed_transform[0]}, {transformed_transform[4]})")
                    print(f"  Dimensions: {transformed_src.width} x {transformed_src.height}")
                    print(f"  Bounds: {transformed_bounds}")
    
                    # # Step 4: Plot the rasters for comparison
                    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
                    # # Plot reference raster
                    # show(reference_data, transform=reference_transform, ax=ax1, title='Reference Raster')
                    # ax1.set_xlabel('X Coordinate')
                    # ax1.set_ylabel('Y Coordinate')
    
                    # # Plot original first raster
                    # show(first_data, transform=first_transform, ax=ax2, title='Original First Raster')
                    # ax2.set_xlabel('X Coordinate')
                    # ax2.set_ylabel('Y Coordinate')
    
                    # Plot superimposed rasters in the third plot
                    # Calculate the extent for both rasters in the same coordinate system
                    ref_extent = [reference_bounds.left, reference_bounds.right, 
                                 reference_bounds.bottom, reference_bounds.top]
                    trans_extent = [transformed_bounds.left, transformed_bounds.right, 
                                   transformed_bounds.bottom, transformed_bounds.top]
    
                    # Determine the common extent for visualization
                    common_extent = [
                        min(ref_extent[0], trans_extent[0]),
                        max(ref_extent[1], trans_extent[1]),
                        min(ref_extent[2], trans_extent[2]),
                        max(ref_extent[3], trans_extent[3])
                    ]
    
                    # Create a masked array for the reference data to handle nodata values
                    ref_masked = np.ma.masked_equal(reference_data, reference_meta.get('nodata', 0))
    
                    # Create a masked array for the transformed data to handle nodata values
                    trans_masked = np.ma.masked_equal(transformed_data, first_meta.get('nodata', 0))
    
                    # Plot reference raster in blue
                    # ax3.imshow(ref_masked, extent=ref_extent, cmap='Blues', alpha=0.7, 
                    #           interpolation='nearest', origin='upper')
    
                    # # Plot transformed raster in red
                    # ax3.imshow(trans_masked, extent=trans_extent, cmap='Reds', alpha=0.7,
                    #           interpolation='nearest', origin='upper')
    
                    # # Set the extent to show both rasters
                    # ax3.set_xlim(common_extent[0], common_extent[1])
                    # ax3.set_ylim(common_extent[2], common_extent[3])
    
                    # ax3.set_title('Superimposed: Reference (Blue) & Transformed (Red)')
                    # ax3.set_xlabel('X Coordinate')
                    # ax3.set_ylabel('Y Coordinate')
    
                    # Create custom patches for the legend
                    # from matplotlib.patches import Patch
                    # legend_elements = [
                    #     Patch(facecolor='blue', alpha=0.7, label='Reference Raster'),
                    #     Patch(facecolor='red', alpha=0.7, label='Transformed Raster')
                    # ]
                    # ax3.legend(handles=legend_elements, loc='upper right')
    
                    # plt.tight_layout()
                    # plt.show()
    
                    # print("\nPlots shown. The third plot shows both rasters superimposed.")
                    # print("If the origin points are properly aligned, the features should line up correctly.")
    
                    # Optional: Save the transformed raster permanently
                    # Uncomment the following line to save the transformed raster
                    shutil.copy2(temp_output, os.path.join(input_folder, f"transformed_{first_raster_name}"))
        
        os.rename(os.path.join(input_folder, f"{first_raster_name}"),
                  os.path.join(input_folder, f"original_{first_raster_name}"))
        
        crop_raster_to_reference(reference_raster_path,
                                 os.path.join(input_folder, f"transformed_{first_raster_name}"),
                                 os.path.join(input_folder, f"{first_raster_name}"))
        
        os.remove(os.path.join(input_folder, f"transformed_{first_raster_name}"))