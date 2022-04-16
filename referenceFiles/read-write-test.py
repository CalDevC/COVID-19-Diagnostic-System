import SimpleITK as sitk

reader = sitk.ImageFileReader()
# For DICOM Image
# reader.SetImageIO("GDCMImageIO")
# reader.SetFileName("images/chest.dcm")
reader.SetImageIO("PNGImageIO")
reader.SetFileName("images/sphere.png")
image = reader.Execute()

writer = sitk.ImageFileWriter()
# For DICOM Image
# writer.SetFileName("images/new_chest.dcm")
writer.SetFileName("images/new_sphere.png")
writer.Execute(image)