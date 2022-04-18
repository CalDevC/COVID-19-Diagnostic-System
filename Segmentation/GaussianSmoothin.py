#!/usr/bin/env python

import SimpleITK as sitk
import argparse
import os

parser = argparse.ArgumentParser(description="Rescales image to grayscale and smoothes while perserving edges")
parser.add_argument("input_image")
parser.add_argument("output_image")
args = parser.parse_args()

reader = sitk.ImageFileReader()
reader.SetFileName(args.input_image)
image = reader.Execute()

BilateralFilter = sitk.BilateralImageFilter()
BilateralFilter.SetDomainSigma(0.1)
BilateralFilter.SetRangeSigma(0.1)
image = BilateralFilter.Execute(image)


rescaler = sitk.RescaleIntensityImageFilter()
rescaler.SetOutputMinimum(0)
rescaler.SetOutputMaximum(255)
image = rescaler.Execute(image)

writer = sitk.ImageFileWriter()
writer.SetFileName(args.output_image)
writer.Execute(image)
