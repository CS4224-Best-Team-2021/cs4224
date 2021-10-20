# Set variables for the servers here.
# Create aliases for all servers
SERVER1="192.168.48.169" 
SERVER2="192.168.48.170" 
SERVER3="192.168.48.171" 
SERVER4="192.168.48.172" 
SERVER5="192.168.48.173"

# Set LAN address and ports
declare -A ports
ports[$SERVER1]=5001
ports[$SERVER2]=5002
ports[$SERVER3]=5003
ports[$SERVER4]=5004
ports[$SERVER5]=5005

# Set the store names of each db
declare -A storenames
storenames[$SERVER1]="store1" 
storenames[$SERVER2]="store2" 
storenames[$SERVER3]="store3" 
storenames[$SERVER4]="store4" 
storenames[$SERVER5]="store5"

# Set the http addresses
declare -A https
https[$SERVER1]=9000
https[$SERVER2]=9002
https[$SERVER3]=9003
https[$SERVER4]=9004
https[$SERVER5]=9005

# Set cert directories
declare -A certs
certs[$SERVER1]="certs1" 
certs[$SERVER2]="certs2" 
certs[$SERVER3]="certs3" 
certs[$SERVER4]="certs4" 
certs[$SERVER5]="certs5"
