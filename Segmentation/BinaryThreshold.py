#!/usr/bin/env python

import SimpleITK as sitk
import os

def binThreshold(input_image, output_image, lower_threshold, upper_threshold, inside_value, outside_value):
    PixelType = sitk.sitkFloat32
    #Read the image that the threshold will be applied to
    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")
    reader.SetFileName(input_image)
    image = reader.Execute()
    #Threshold the image 
    thresholdFilter = sitk.BinaryThresholdImageFilter()
    #Lower Threshold is the lowest pixel value in the range of pixels that the threshold will be applied too
    thresholdFilter.SetLowerThreshold(lower_threshold)
    #Upper Threshold is the highest pixel value in the range of pixels that the threshold will be applied too
    thresholdFilter.SetUpperThreshold(upper_threshold)
    #Whatever pixels values that arent in the range of lower to upper threshold value will be set to this color value
    thresholdFilter.SetOutsideValue(outside_value)
    #Whatever pixels values that are in the range of lower to upper threshold value will be set to this color value
    thresholdFilter.SetInsideValue(inside_value)
    image = thresholdFilter.Execute(image)
    
    #Write out a new image that has been thresholded 
    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_image)
    writer.Execute(image)

    if ("SITK_NOSHOW" not in os.environ):
        os.environ.setdefault("SITK_SHOW_EXTENSION", ".nii")
        NIfTIReader = sitk.ImageFileReader()
        NIfTIReader.SetImageIO("NiftiImageIO")
        NIfTIReader.SetFileName(output_image)
        image = NIfTIReader.Execute()

        #Display the image using ImageJ
        sitk.Show(image, "Segmented_Image")
