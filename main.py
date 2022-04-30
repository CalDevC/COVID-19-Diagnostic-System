from cgi import print_directory
from Registration.registration import reg
from Segmentation import *
import SimpleITK as sitk
import os

from Segmentation.BilateralSmoothing import biLatSmooth
from Segmentation.BinaryThreshold import binThreshold

# Main driver code here
negPathTemplate = "images/negativePatients/negPatient"
startingNegPatient = "images/negativePatients/negPatient4"
normalPatientNIfTI = "images/sample.nii"

testPatient = "images/patient1"
testPatientNIfTI = "images/testPatient.nii"

finalOutput = "images/final.nii"

reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", startingNegPatient)
dicom_names = reader.GetGDCMSeriesFileNames(startingNegPatient)
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), normalPatientNIfTI)

print("Starting on normalized image")

for i in range(5, 6):
    print("Using " + str(i))
    reg(normalPatientNIfTI, negPathTemplate + str(i), normalPatientNIfTI)

print("Starting on Segmentation")

#Create a NIfTI image from the test patient
print("Reading DICOM files from directory: ", testPatient)
dicom_names = reader.GetGDCMSeriesFileNames(testPatient)
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), testPatientNIfTI)

binThreshold(testPatientNIfTI, testPatientNIfTI, 0, 255)
biLatSmooth(testPatientNIfTI, testPatientNIfTI)

if ("SITK_NOSHOW" not in os.environ):
    os.environ.setdefault("SITK_SHOW_EXTENSION", ".nii")
    NIfTIReader = sitk.ImageFileReader()
    NIfTIReader.SetImageIO("NiftiImageIO")
    NIfTIReader.SetFileName(testPatientNIfTI)
    image = NIfTIReader.Execute()

    #Display the image using ImageJ
    sitk.Show(image, "Segmented_Image")

reg(normalPatientNIfTI, testPatientNIfTI, finalOutput)