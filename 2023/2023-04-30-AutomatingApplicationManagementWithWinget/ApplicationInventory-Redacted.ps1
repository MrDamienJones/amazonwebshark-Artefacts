'''
Script creates two files:  

- AppInventory-WingetExport can be used to duplicate setup on new hardware and VMs.
- AppInventory-WingetList contains applications not included in AppInventory-WingetExport.
- Files are saved to OneDrive
'''

#########################
### WINDOWS VARIABLES ###
#########################

# Capture date & time for distinct filenames
$RunDate = Get-Date -Format 'yyyy-MM-dd-HHmm'


#####################
### WINGET EXPORT ###
#####################

# File path for objects
$ExportsFilePath = 'C:\{Path}\AppInventory-Exports'

# File name structure
$ExportsFileName = 'WingetExport' + '-' + $env:computername + '-'

# winget export output parameter
$ExportsOutput = $ExportsFilePath + '\' + $ExportsFileName  + $RunDate + '.json'

# winget export command
winget export --output $ExportsOutput --include-versions


###################
### WINGET LIST ###
###################

# File path for objects
$ListsFilePath = 'C:\{Path}\AppInventory-Lists'

# File name structure
$ListsFileName = 'WingetList' + '-' + $env:computername + '-'

# winget list Out-File parameter
$ListsOutput = $ListsFilePath + '\' + $ListsFileName + $RunDate + '.txt'

# winget list command
winget list | Out-File -FilePath $ListsOutput