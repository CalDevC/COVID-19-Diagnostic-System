#!/usr/bin/env python

import itk
import argparse

parser = argparse.ArgumentParser(description="Computes Smoothing With Gaussian Kernel.")
parser.add_argument("input_image")
parser.add_argument("output_image")
args = parser.parse_args()

InputPixelType = itk.F
OutputPixelType = itk.UC
Dimension = 3


InputImageType = itk.Image[InputPixelType, Dimension]
OutputImageType = itk.Image[OutputPixelType, Dimension]

reader = itk.ImageFileReader[InputImageType].New()
reader.SetFileName(args.input_image)

smoothFilter = itk.SmoothingRecursiveGaussianImageFilter.New(reader)
smoothFilter.SetSigma(2)

rescaler = itk.RescaleIntensityImageFilter[InputImageType, OutputImageType].New()
rescaler.SetInput(smoothFilter.GetOutput())
rescaler.SetOutputMinimum(0)
rescaler.SetOutputMaximum(255)

writer = itk.ImageFileWriter[OutputImageType].New()
writer.SetFileName(args.output_image)
writer.SetInput(rescaler.GetOutput())

writer.Update()
