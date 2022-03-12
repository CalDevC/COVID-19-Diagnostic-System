# COVID-19-Diagnostic-System



### Registration temporary notes
To make ImageJ display the image properly you need to set certain environment variables. CHeck these variables using below commands:
 - `$Env:SITK_SHOW_EXTENSION` (should display .png)
 - `$Env:SITK_SHOW_COMMAND` (Should display path to ImageJ.exe)

These variables can be set in PowerShell using:
 - `$Env:SITK_SHOW_EXTENSION = "<image-type>"`
 - `$Env:SITK_SHOW_EXTENSION = "<path-to-imagej.exe>"`