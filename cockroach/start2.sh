# Create aliases for all servers
SERVER1="192.168.48.169" 
SERVER2="192.168.48.170" 
SERVER3="192.168.48.171" 
SERVER4="192.168.48.172" 
SERVER5="192.168.48.173"

# Create a hash table for LAN address and ports
declare -A ports
ports[$SERVER1]=5001
ports[$SERVER2]=5002
ports[$SERVER3]=5003
ports[$SERVER4]=5004
ports[$SERVER5]=5005

# Create a hash table for the store names of each db
declare -A storenames
storenames[$SERVER1]="store1" 
storenames[$SERVER2]="store2" 
storenames[$SERVER3]="store3" 
storenames[$SERVER4]="store4" 
storenames[$SERVER5]="store5"

# Create a hash table for the http addresses
declare -A https
https[$SERVER1]=9001
https[$SERVER2]=9002
https[$SERVER3]=9003
https[$SERVER4]=9004
https[$SERVER5]=9005


# Get the specific variables of this machine
HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}
STORE=${storenames[$HOST_NAME]}
HTTP_PORT=${https[$HOST_NAME]}

# Confirm to the user which IP address and port this machine will advertise and listen on
echo "This machine will advertise and listen on the address: $HOST_NAME:$PORT"

# Ask if cluster has been initialised
read -p "Type 'yes' if you need to run cockroach init, or hit the Enter key otherwise: " response

# NOTE: You must use the same port configurations on all servers.
cockroach start \
--insecure \
--listen-addr=$HOST_NAME:$PORT \
--join=$SERVER1:$PORT_1,$SERVER2:$PORT_2,$SERVER3:$PORT_3,$SERVER4:$PORT_4,$SERVER5:$PORT_5 \
--cache=.25 \
--max-sql-memory=.25 \
--background \
--store=$STORE \
--http-addr=$HOST_NAME:$HTTP_PORT

# if response='yes' 
# then 
#     cockroach init --insecure --host=$HOST_NAME:$PORT
# fi
