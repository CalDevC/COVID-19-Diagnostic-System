
import SimpleITK as sitk
import vtk
import sys
import os

viewer = sitk.ImageViewer()
viewer.SetFileExtension('.nii')
viewer.SetCommand('C:\Program Files\ImageJ\ImageJ.exe')

if len(sys.argv) < 3:
    print("Usage: DicomSeriesReader <input_directory> <output_file>")
    sys.exit(1)

print("Reading Dicom directory:", sys.argv[1])
reader = sitk.ImageSeriesReader()

dicom_names = reader.GetGDCMSeriesFileNames(sys.argv[1])
reader.SetFileNames(dicom_names)

image = reader.Execute()

size = image.GetSize()
print("Image size:", size[0], size[1], size[2])

print("Writing image:", sys.argv[2])

sitk.WriteImage(image, sys.argv[2])


viewer.Execute(image)