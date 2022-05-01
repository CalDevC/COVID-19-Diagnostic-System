#!/usr/bin/env python

import SimpleITK as sitk
import argparse
import os

# parser = argparse.ArgumentParser(description="Threshold An Image Using Binary.")
# parser.add_argument("input_image")
# parser.add_argument("output_image")
# parser.add_argument("lower_threshold", type=int)
# parser.add_argument("upper_threshold", type=int)

# args = parser.parse_args()

def binThreshold(input_image, output_image, lower_threshold, upper_threshold, inside_value):
    PixelType = sitk.sitkFloat32

    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")
    reader.SetFileName(input_image)
    image = reader.Execute()

    thresholdFilter = sitk.BinaryThresholdImageFilter()
    thresholdFilter.SetLowerThreshold(lower_threshold)
    thresholdFilter.SetUpperThreshold(upper_threshold)
    thresholdFilter.SetOutsideValue(0)
    thresholdFilter.SetInsideValue(inside_value)
    image = thresholdFilter.Execute(image)

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
