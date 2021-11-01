# Temporary fix to make certs folder executable

for i in {1..5}
do 
    cp certs$i certs${i}temp # copy the folder to a temp folder
    rm -rf certs$i # remove the original
    cp certs${i}temp certs$i # copy the temp into the original
    rm -rf certs${i}temp # remove the temp folder
done