#!/usr/bin/env python

import itk
import argparse

parser = argparse.ArgumentParser(description="Threshold An Image Using Binary.")
parser.add_argument("input_image")
parser.add_argument("output_image")
parser.add_argument("lower_threshold", type=int)
parser.add_argument("upper_threshold", type=int)

args = parser.parse_args()

PixelType = itk.UC
Dimension = 3

ImageType = itk.Image[PixelType, Dimension]

reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName(args.input_image)

thresholdFilter = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()
thresholdFilter.SetInput(reader.GetOutput())

thresholdFilter.SetLowerThreshold(args.lower_threshold)
thresholdFilter.SetUpperThreshold(args.upper_threshold)
thresholdFilter.SetOutsideValue(0)
thresholdFilter.SetInsideValue(255)

writer = itk.ImageFileWriter[ImageType].New()
writer.SetFileName(args.output_image)
writer.SetInput(thresholdFilter.GetOutput())

writer.Update()