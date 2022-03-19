import SimpleITK as sitk
import vtk as vtk
import math
import sys
import os

# Set up image viewer with proper settings
os.environ.setdefault("SITK_SHOW_EXTENSION", ".nii")

def command_iteration(method):
    if (method.GetOptimizerIteration() == 0):
        print("Estimated Scales: ", method.GetOptimizerScales())
    print(f"{method.GetOptimizerIteration():3} = {method.GetMetricValue():7.5f} : {method.GetOptimizerPosition()}")


fixedDir = "images/patient1"
movingDir = "images/patient2"
transformFile = "transform.txt"
outputFile = "images/new.nii"

reader = sitk.ImageSeriesReader()
print("Reading Dicom directory:", fixedDir)
dicom_names = reader.GetGDCMSeriesFileNames(fixedDir)
reader.SetFileNames(dicom_names)
sitk.WriteImage(reader.Execute(), "images/fixed.nii")

reader2 = sitk.ImageSeriesReader()
print("Reading Dicom directory:", movingDir)
dicom_names = reader2.GetGDCMSeriesFileNames(movingDir)
reader2.SetFileNames(dicom_names)
sitk.WriteImage(reader2.Execute(), "images/moving.nii")


pixelType = sitk.sitkFloat32
fixedImage = sitk.ReadImage("images/fixed.nii", pixelType, )
movingImage = sitk.ReadImage("images/moving.nii", pixelType)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsMeanSquares()
# R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
R.SetOptimizerAsGradientDescent(learningRate=2.0, numberOfIterations=200)
R.SetInitialTransform(sitk.TranslationTransform(fixedImage.GetDimension()))
R.SetInterpolator(sitk.sitkLinear)

R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R))

outTx = R.Execute(fixedImage, movingImage)

print("-------")
print(outTx)
print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
print(f" Iteration: {R.GetOptimizerIteration()}")
print(f" Metric value: {R.GetMetricValue()}")

sitk.WriteTransform(outTx, transformFile)

if ("SITK_NOSHOW" not in os.environ):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixedImage)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(100)
    resampler.SetTransform(outTx)

    out = resampler.Execute(movingImage)
    simg1 = sitk.Cast(sitk.RescaleIntensity(fixedImage), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)

    # Save image as new.png
    writer = sitk.ImageFileWriter()
    writer.SetFileName("images/transformedImage.nii")
    writer.Execute(cimg)

    #Display the image using ImageJ
    sitk.Show(cimg, "Transformed Image")