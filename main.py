from Registration.registration import reg
import SimpleITK as sitk

# Main driver code here

reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", "images/negativePatients/negPatient1")
dicom_names = reader.GetGDCMSeriesFileNames("images/negativePatients/negPatient1")
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), "images/sample.nii")

print("Starting on normalized image")

for i in range(2, 10):
    reg("images/sample.nii", f"images/negativePatients/negPatient{i}", "images/sample.nii")