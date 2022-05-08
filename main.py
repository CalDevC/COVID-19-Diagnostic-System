from cgi import print_directory
from Registration.registration import reg
from Segmentation import *
import SimpleITK as sitk

from Segmentation.BilateralSmoothing import biLatSmooth
from Segmentation.BinaryThreshold import binThreshold

# Paths to images/directories
normalPatient = "images/healthyLung"
normalPatientNIfTI = "images/healthy.nii"
normalPatientSegNIfTI = "images/healthySeg.nii"
testPatientNIfTI = "images/covidLung.nii"
finalOutput = "images/final.nii"

# Read the DICOM series of the normal patient and save it as a NIfTI file
reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", normalPatient)
dicom_names = reader.GetGDCMSeriesFileNames(normalPatient)
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), normalPatientNIfTI)

#The below code is needed only if the test patient scan is in DICOM format
# #Create a NIfTI image from the test patient
# testPatient = "images/"
# print("Reading DICOM files from directory: ", testPatient)
# dicom_names = reader.GetGDCMSeriesFileNames(testPatient)
# reader.SetFileNames(dicom_names)
# sitk.WriteImage(reader.Execute(), testPatientNIfTI)

print("Starting on Segmentation")
# Perform segmentation on the healthy patient
biLatSmooth(normalPatientNIfTI, normalPatientSegNIfTI)
binThreshold(normalPatientSegNIfTI, normalPatientSegNIfTI, 80, 120, 100, 0)

# Perform segmentation on the test patient
biLatSmooth(testPatientNIfTI, finalOutput)
binThreshold(finalOutput, finalOutput, 35, 45, 50, 0)
print("Segmentation Complete!")

print("Starting on Registration")
# Register the 2 segmented images
reg(normalPatientSegNIfTI, finalOutput, finalOutput)
print("Registration Complete!")