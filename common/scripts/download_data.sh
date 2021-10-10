#########################################
# Script to download project data files #
#########################################

# Remove the current data 
rm -rf project_files_3

# Get the zip file
wget http://www.comp.nus.edu.sg/~cs4224/project_files_3.zip

# Unzip into a folder
unzip project_files_3.zip -d ..

# Delete the zip file
rm project_files_3.zip