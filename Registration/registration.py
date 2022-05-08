import SimpleITK as sitk
import os

def reg(fixedDirPath, movingDirPath, outputDirPath):
    # Set up image viewer (ImageJ) with proper settings
    os.environ.setdefault("SITK_SHOW_EXTENSION", ".nii")

    # File used to write the transform
    transformFile = "transform.txt"

    # Use imageSeriesReader to read directory of DICOM images in as 3D images (nii format)
    reader = sitk.ImageSeriesReader()
    pixelType = sitk.sitkFloat32

    # Determine if the path to the fixed image is a directory of DICOMs 
    # or a previously generated nii image
    if fixedDirPath.split(".")[-1] == "nii":
        fixedImage = sitk.ReadImage(fixedDirPath, pixelType)
    else:  # If path is a direecctory of DICOMs
        print("Reading DICOM files from directory: ", fixedDirPath)
        dicom_names = reader.GetGDCMSeriesFileNames(fixedDirPath)
        reader.SetFileNames(dicom_names)
        sitk.WriteImage(reader.Execute(), "images/fixed.nii")
        fixedImage = sitk.ReadImage("images/fixed.nii", pixelType)

    if movingDirPath.split(".")[-1] == "nii":
        movingImage = sitk.ReadImage(movingDirPath, pixelType)
    else:  # If path is a direecctory of DICOMs
        print("Reading DICOM files from directory: ", movingDirPath)
        dicom_names = reader.GetGDCMSeriesFileNames(movingDirPath)
        reader.SetFileNames(dicom_names)
        # Read in the newly generated moving image (3D)
        movingImage = sitk.ReadImage("images/moving.nii", pixelType)

    # Number of histogram bins used to compute the entropy
    numberOfBins = 24
    samplingPercentage = 0.10

    # Create our desired registration method
    regMethod = sitk.ImageRegistrationMethod()

    # Similarity metric
    regMethod.SetMetricAsMattesMutualInformation(numberOfBins)
    regMethod.SetMetricSamplingPercentage(samplingPercentage, sitk.sitkWallClock)
    regMethod.SetMetricSamplingStrategy(regMethod.RANDOM)

    # Optimizer
    regMethod.SetOptimizerAsOnePlusOneEvolutionary(numberOfIterations=200)

    # Transform
    regMethod.SetInitialTransform(sitk.CenteredTransformInitializer(fixedImage, movingImage, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY))
    regMethod.SetInterpolator(sitk.sitkLinear)

    # Generate the transform
    outTx = regMethod.Execute(fixedImage, movingImage)

    # Print transform along with registration method informatoin
    print("=======================================================")
    print(f"Optimizer stop condition: {regMethod.GetOptimizerStopConditionDescription()}")
    print(f" Iteration: {regMethod.GetOptimizerIteration()}")
    print(f" Metric value: {regMethod.GetMetricValue()}")

    # Write the transform to the transform filw
    sitk.WriteTransform(outTx, transformFile)

    # If we aren't requested to not show the image
    if ("SITK_NOSHOW" not in os.environ):
        # Set up resampler
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixedImage)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(100)
        resampler.SetTransform(outTx)

        # Run the resampler
        out = resampler.Execute(movingImage)
        simg1 = sitk.Cast(sitk.RescaleIntensity(fixedImage), sitk.sitkUInt8)
        simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)

        # Create the final output
        cimg = simg1 // 2. + simg2 // 2.

        # Save image as transformedImage in nii format
        writer = sitk.ImageFileWriter()
        writer.SetFileName(outputDirPath)
        writer.Execute(cimg)

        #Display the image using ImageJ
        sitk.Show(cimg, "Transformed_Image")