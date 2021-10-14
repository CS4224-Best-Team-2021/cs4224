# Get the LAN address of this machine
HOST_NAME="$( hostname -i )"

# Prompt for a port to use
read -p "Enter port to advertise and listen on: " PORT

# Confirm to the user which IP address and port this machine will advertise and listen on
echo "This machine will advertise and listen on the address: $HOST_NAME:$PORT"

# Start CockroachDB, with all ports set to PORT. 
# NOTE: You must use the same port number on all servers.
cockroach start \
--insecure \
--listen-addr=$HOST_NAME:$PORT \
--join=192.168.48.169:$PORT,192.168.48.170:$PORT,192.168.48.171:$PORT,192.168.48.172:$PORT,192.168.48.173:$PORT \
--cache=.25 \
--max-sql-memory=.25 \
--background


# Initialise the cluster with xcnc20 as the host, and port set to PORT.
cockroach init --insecure --host=192.168.48.169:$PORT