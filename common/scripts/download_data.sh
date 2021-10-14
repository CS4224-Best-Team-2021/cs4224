#########################################
# Script to download project data files #
#########################################

# Get the location of this script
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Remove the current data 
rm -rf $SCRIPT_DIR/project_files_4

# Get the zip file
wget http://www.comp.nus.edu.sg/~cs4224/project_files_4.zip

# Unzip into a folder
unzip project_files_4.zip -d $SCRIPT_DIR/..

# Delete the zip file
rm project_files_4.zip