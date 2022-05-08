#!/usr/bin/env python

import SimpleITK as sitk
import argparse
import os

# parser = argparse.ArgumentParser(description="Rescales image to grayscale and smoothes while perserving edges")
# parser.add_argument("input_image")
# parser.add_argument("output_image")
# args = parser.parse_args()

def biLatSmooth(input_image, output_image):
    reader = sitk.ImageFileReader()
    reader.SetFileName(input_image)
    image = reader.Execute()
    
    
    rescaler = sitk.RescaleIntensityImageFilter()
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)
    image = rescaler.Execute(image)
    
    BilateralFilter = sitk.BilateralImageFilter()
    BilateralFilter.SetDomainSigma(0.8)
    BilateralFilter.SetNumberOfRangeGaussianSamples(20)
    BilateralFilter.SetRangeSigma(10.0)
    image = BilateralFilter.Execute(image)

    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_image)
    writer.Execute(image)
