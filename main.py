from cgi import print_directory
from Registration.registration import reg
import SimpleITK as sitk

# Main driver code here
startingDir = "images/negativePatients/negPatient1"

reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", startingDir)
dicom_names = reader.GetGDCMSeriesFileNames(startingDir)
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), "images/sample.nii")

print("Starting on normalized image")

for i in range(2, 3):
    print("Using " + str(i))
    reg("images/sample.nii", f"images/negativePatients/negPatient{i}", "images/sample.nii")