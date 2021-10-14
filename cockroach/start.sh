# Get ports of every server
read -p "xcnc20 port number: " PORT_1
read -p "xcnc21 port number: " PORT_2
read -p "xcnc22 port number: " PORT_3
read -p "xcnc23 port number: " PORT_4
read -p "xcnc24 port number: " PORT_5

# Create a hash table for LAN address and ports
declare -A ports
ports["192.168.48.169"]=$PORT_1 
ports["192.168.48.170"]=$PORT_2 
ports["192.168.48.171"]=$PORT_3 
ports["192.168.48.172"]=$PORT_4 
ports["192.168.48.173"]=$PORT_5

# Get the LAN address of this machine
HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}

# Confirm to the user which IP address and port this machine will advertise and listen on
echo "This machine will advertise and listen on the address: $HOST_NAME:$PORT"

# Ask if cluster has been initialised
read -p "Type 'yes' if you need to run cockroach init" response


# NOTE: You must use the same port configurations on all servers.
cockroach start \
--insecure \
--listen-addr=$HOST_NAME:$PORT \
--join=192.168.48.169:$PORT_1,192.168.48.170:$PORT_2,192.168.48.171:$PORT_3,192.168.48.172:$PORT_4,192.168.48.173:$PORT_5 \
--cache=.25 \
--max-sql-memory=.25 \
--background


if response='yes' 
then 
    cockroach init --insecure --host=192.168.48.169:$PORT_1
fi
