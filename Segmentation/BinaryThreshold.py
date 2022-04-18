#!/usr/bin/env python

import SimpleITK as sitk
import argparse
import os

parser = argparse.ArgumentParser(description="Threshold An Image Using Binary.")
parser.add_argument("input_image")
parser.add_argument("output_image")
parser.add_argument("lower_threshold", type=int)
parser.add_argument("upper_threshold", type=int)

args = parser.parse_args()

PixelType = sitk.sitkFloat32

reader = sitk.ImageFileReader()
reader.SetImageIO("NiftiImageIO")
reader.SetFileName(args.input_image)
image = reader.Execute()

thresholdFilter = sitk.BinaryThresholdImageFilter()
thresholdFilter.SetLowerThreshold(args.lower_threshold)
thresholdFilter.SetUpperThreshold(args.upper_threshold)
thresholdFilter.SetOutsideValue(0)
thresholdFilter.SetInsideValue(255)
image = thresholdFilter.Execute(image)

writer = sitk.ImageFileWriter()
writer.SetFileName(args.output_image)
writer.Execute(image)
