from cgi import print_directory
from Registration.registration import reg
from Segmentation import *
import SimpleITK as sitk

from Segmentation.BilateralSmoothing import biLatSmooth
from Segmentation.BinaryThreshold import binThreshold

startingNegPatient = "images/healthyLung"
normalPatientNIfTI = "images/healthy.nii"
normalPatientSegNIfTI = "images/healthySeg.nii"

testPatientNIfTI = "images/covidLung.nii"

finalOutput = "images/final.nii"

reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", startingNegPatient)
dicom_names = reader.GetGDCMSeriesFileNames(startingNegPatient)
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
biLatSmooth(normalPatientNIfTI, normalPatientSegNIfTI)
binThreshold(normalPatientSegNIfTI, normalPatientSegNIfTI, 80, 120, 100, 0)

biLatSmooth(testPatientNIfTI, finalOutput)
binThreshold(finalOutput, finalOutput, 35, 45, 50, 0)
print("Segmentation Complete!")

print("Starting on Registration")
reg(normalPatientSegNIfTI, finalOutput, finalOutput)
print("Registration Complete!")