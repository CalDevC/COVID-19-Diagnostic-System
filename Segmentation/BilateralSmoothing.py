#!/usr/bin/env python

import SimpleITK as sitk

def biLatSmooth(input_image, output_image):
    #Used to read the 3D image file that will have the filter applied to
    reader = sitk.ImageFileReader()
    reader.SetFileName(input_image)
    image = reader.Execute()
    
    #rescale the image to grayscale 0,255 for thresholding
    rescaler = sitk.RescaleIntensityImageFilter()
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)
    image = rescaler.Execute(image)
    
    #Creating the bilateral Filter from SimpleITK
    BilateralFilter = sitk.BilateralImageFilter()
    #Two sigma values the domain sigma should be set lower than the range generally up to 10 times lower
    BilateralFilter.SetDomainSigma(0.8)
    #Number of range gaussians range from 0 - 4*RangeSigma
    BilateralFilter.SetNumberOfRangeGaussianSamples(20)
    BilateralFilter.SetRangeSigma(10.0)
    image = BilateralFilter.Execute(image)

    #write a new image with the filter applied to
    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_image)
    writer.Execute(image)
