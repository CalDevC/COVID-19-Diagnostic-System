from Registration.registration import reg
import SimpleITK as sitk

# Main driver code here

reader = sitk.ImageSeriesReader()
print("Reading DICOM files from directory: ", "images/negPatient1")
dicom_names = reader.GetGDCMSeriesFileNames("images/negPatient1")
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), "images/sample.nii")

for i in range(2, 10):
    reg("images/sample.nii", f"images/negativePatients/nagPatient{i}", "images/sample.nii")